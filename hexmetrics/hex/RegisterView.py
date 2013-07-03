import random, string

from flask import url_for, render_template, flash, redirect, make_response, request
from flask.ext.classy import FlaskView, route

from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, HiddenField
from flask.ext.wtf import Required
from flask.ext.wtf import EqualTo, Email

from flask.ext.login import login_user

from main import db, app

from models import User, UserSignupDetails, ROLE_USER, USER_ACTIVE

import requests


class RegisterForm(Form):
    username = TextField('username', validators = [Required()])
    realname = TextField('realname', validators = [Required()])
    password = PasswordField('password', validators = [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm =  PasswordField('confirm')
    email = TextField('email', validators = [Required(), Email()])
    havereadtos = BooleanField('havereadtos', default = False)
    destpage = HiddenField('destpage')
    
    def validate_on_submit(self):
        superVal = super(RegisterForm, self).validate_on_submit()
        customVal = True
        if not self.havereadtos.data:
            self.havereadtos.errors.append('You must read and agree to Terms of Use before continuing.')
            customVal = False;
        if User.query.filter_by(username = self.username.data).first() is not None:
            self.username.errors.append('Username is already in use.')
            customVal = False;
        else:
            newUser = User(username=self.username.data, email=self.email.data, password=self.password.data, realname=self.realname.data, role=ROLE_USER)
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
            newUser.signUpDetails.append(UserSignupDetails(signupKey=key, destPage=self.destpage.data))

            mailDetails = {'from': app.config['EMAIL_FROM'],
                           'from_name': app.config['EMAIL_FROM_NAME'],
                           'to': [newUser.email],
                           'bcc': app.config['EMAIL_ADMINS'],
                           'subject': "Thank you for signing up at HEX Metrics.",
                           'text': "Thank you for signing up at HEX Metrics.\n\nPlease use the following URL to confirm your account: http://{u}/register/c/{k}".format(k=key,u=app.config['SERVER_NAME']),
                           
                           }

            try:
                requests.post(
                              app.config['EMAIL_MAILGUN_API_URL'],
                              auth=("api", app.config['EMAIL_MAILGUN_API_KEY']),
                              data={"from": '%s <%s>' % (mailDetails['from_name'], mailDetails['from']),
                                    "to": mailDetails['to'],
                                    "bcc": mailDetails['bcc'],
                                    "subject": mailDetails['subject'],
                                    "text": mailDetails['text']
                                    })
            except:
                try:
                    import smtplib
                    smtpObj = smtplib.SMTP(app.config['EMAIL_SMTP_SERVER'],587)
                    msg = "From: %s <%s>\r\n" % (mailDetails['from_name'], mailDetails['from']) \
                        + "To: %s\r\n" % mailDetails['to']                                      \
                        + "Bcc: %s\r\n" % ','.join(app.config['EMAIL_ADMINS'])                  \
                        + "Subject: %s\r\n" % (mailDetails['subject'])                          \
                        + "\r\n%s" % mailDetails['text']
                    smtpObj.set_debuglevel(1)
                    print msg
                    smtpObj.login(app.config['EMAIL_SMTP_USER'], app.config['EMAIL_SMTP_PASS'])
                    smtpObj.sendmail(app.config['EMAIL_FROM'], [mailDetails['to']] + app.config['EMAIL_ADMINS'], msg)
                    smtpObj.quit()
                    
                except:
                    
                    self.email.errors.append('Unable to send email!')
                    return False
                
            db.session.add(newUser)
            db.session.commit()

        return superVal and customVal
        

class RegisterView(FlaskView):
    
    def index(self):
        form = RegisterForm();
        form.destpage.data = request.args.get("destpage");
        return render_template('register.html', form=form);

    def thankyou(self):
        return render_template('thankyou.html');
    
    def post(self):
        form = RegisterForm();
        if form.validate_on_submit():
            response = make_response(redirect(url_for('RegisterView:thankyou')))
            response.headers['X-Requested-With'] = form.csrf_token.data
            return response
        return render_template('register.html', form=form);
    
    @route('/c/<key>')
    def confirm(self, key):
        details = UserSignupDetails.query.filter_by(signupKey=key).first()
        user = User.query.filter_by(id=details.detailsFor).first()
        user.active = USER_ACTIVE
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(u'Your account is now active.<br />Please log in.', 'success')
        if details is not None:
            return redirect(details.destPage or url_for('IndexView:index'))