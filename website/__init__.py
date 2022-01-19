from flask import Flask  
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager


db = SQLAlchemy()
DB_NAME = "company123.db"

def create_app():
    app = Flask(__name__)  
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    from .views import views
    from .authorize import authorize 
    

    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(authorize, url_prefix='/')
    
    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'authorize.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)