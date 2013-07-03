import random, string

from flask import Flask, url_for, render_template, flash, redirect, Response, make_response, request, session
from flask.ext.classy import FlaskView, route

from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, HiddenField
from flask.ext.wtf import Required, ValidationError
from flask.ext.wtf import EqualTo, Email

from flask.ext.login import login_user, logout_user, current_user, login_required

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
            db.session.add(newUser)
            db.session.commit()

            requests.post(
                          app.config['EMAIL_MAILGUN_API_URL'],
                          auth=("api", app.config['EMAIL_MAILGUN_API_KEY']),
                          data={"from": app.config['EMAIL_FROM'],
                                "to": [newUser.email],
                                "bcc": app.config['EMAIL_ADMINS'],
                                "subject": "Thank you for signing up at HEX Metrics.",
                                "text": "Thank you for signing up at HEX Metrics.\n\nPlease use the following URL to confirm your account: http://{u}/register/c/{k}".format(k=key,u=app.config['SERVER_NAME'])
                                })

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
        if details is not None:
            return redirect(details.destPage or url_for('IndexView:index'))