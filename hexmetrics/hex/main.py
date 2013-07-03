import os

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from Logger import HexLogger

app = Flask(__name__, 
            static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'public', 'static')),
            static_url_path = '/static'
            )

try:
    app.config.from_object('hex.config')
except:
    app.config.from_object('config')

HexLogger(app).attach(app);

db = SQLAlchemy(app)

from flask.ext.login import LoginManager

lm = LoginManager()
lm.init_app(app)

lm.login_view = "LoginView:index"

@lm.user_loader
def load_user(userid):
    from models import User
    return User.query.get(userid)

from IndexView import IndexView
from BlogView import BlogView
from LoginView import LoginView
from RegisterView import RegisterView
from ToolsView import ToolsView

IndexView.register(app, route_base='/')
BlogView.register(app, route_base='/blog')
LoginView.register(app, route_base='/login')
RegisterView.register(app, route_base='/register')
ToolsView.register(app, route_base='/tools')

from admin import HexAdmin, HexAdminHome

admin = HexAdmin(index_view=HexAdminHome())
admin.start(app)

@app.errorhandler(Exception)
def generic_error_handler(error):
    app.logger.exception(error)
    from datetime import datetime
    if hasattr(error, 'code'):
        return render_template('error.html', details=error, code=error.code, now=datetime.utcnow()), error.code
    else:
        return render_template('error.html', details=error, code=500, now=datetime.utcnow()), 500
for error in range(400, 420) + range(500,506):
    app.error_handler_spec[None][error] = generic_error_handler

if __name__ == '__main__':

    app.run()