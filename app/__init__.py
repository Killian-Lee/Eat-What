from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'

    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app

@login_manager.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id)) 