from flask import Flask, url_for, render_template, request
from flask.ext.admin import Admin, AdminIndexView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.login import current_user
from flask.ext.admin.contrib.fileadmin import FileAdmin
import os

from flask.ext.wtf import TextArea, TextAreaField, SelectField

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

from main import db, app
from models import *

class HexAdminHome(AdminIndexView):
    def is_accessible(self):
        if current_user.is_anonymous():
            return False;
        return current_user.is_admin()

class HexModelView(ModelView):
    form_excluded_columns = ('created_date')
    
    def is_accessible(self):
        if current_user.is_anonymous():
            return False;
        return current_user.is_admin()

class HexBlogPostView(HexModelView):
    form_overrides = dict(body=CKTextAreaField)
    
    create_template = 'admin/model/edit.html'
    edit_template = 'admin/model/edit.html'
    
class HexUserView(HexModelView):
    column_exclude_list = ('_password')
    form_excluded_columns = ('_password')
    
    form_overrides = dict(role=SelectField, active=SelectField)
    form_args = dict(
                     role=dict(
                               choices=[(0, 'User'), (1, 'Administrator')]
                               ),
                     active=dict(
                                 choices=[(0,'Inactive'), (1, 'Active')]
                                 ),
        )

class HexSnippetView(HexModelView):
    form_overrides = dict(body=CKTextAreaField)
    create_template = 'admin/model/edit.html'
    edit_template = 'admin/model/edit.html'

class HexFileAdmin(FileAdmin):
    def is_accessible(self):
        if current_user.is_anonymous():
            return False;
        return current_user.is_admin()

class HexAdmin(Admin):
    def start(self,app):
        self.init_app(app);
        self.add_view(HexUserView(User, db.session))
        self.add_view(HexBlogPostView(BlogPosts, db.session))
        self.add_view(HexModelView(BlogCategory, db.session))
        self.add_view(HexSnippetView(SnippetLibrary, db.session))
        path = os.path.join(os.path.dirname(__file__), os.pardir, 'public', 'media')
        self.add_view(HexFileAdmin(path, '/static/', name='Static Files'))