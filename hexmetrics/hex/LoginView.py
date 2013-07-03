from flask import Flask, url_for, render_template, flash, redirect, Response, make_response, request
from flask.ext.classy import FlaskView, route

from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, HiddenField
from flask.ext.wtf import Required, ValidationError

from flask.ext.login import login_user, logout_user, current_user, login_required

from models import User

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    next = HiddenField('next')
    
    def validate_on_submit(self):
        superVal = super(LoginForm, self).validate_on_submit()
        customVal = True
        user = User.query.filter_by(username = self.username.data).first()
        if user is None:
            self.username.errors.append('Invalid username.')
            customVal = False;
        else:
            if (user.checkPassword(self.password.data) == False) and (self.password.data != ''):
                self.password.errors.append('Invalid password')
                customVal = False;
            else:
                login_user(user,remember = self.remember_me);
                flash(u'You have been logged in', 'success')
        return superVal and customVal
        

class LoginView(FlaskView):
    def index(self):
        form = LoginForm();
        form.next.data = request.args.get("next");
        return render_template('login.html', form=form);

    def post(self):
        form = LoginForm();
        if form.validate_on_submit():
            response = make_response(redirect(form.next.data or url_for('IndexView:index')))
            response.headers['X-Requested-With'] = form.csrf_token.data
            return response
        return render_template('login.html', form=form);
    
    @login_required
    def logout(self):
        logout_user();
        flash(u'You have been logged out', 'success')
        return make_response(redirect(request.args.get("next") or url_for('IndexView:index')))