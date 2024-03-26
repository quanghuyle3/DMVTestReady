from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "databaseDMV.db"

#initializes and configurates the whole project
def create_app():
    # creating Flask app and setting secret and database configs

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'projectCS122'     #secures cookie data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    # initializing and connecting login manager with our application
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .controller.views import views
    from .controller.auth import auth
    
    # we are letting know app which main routes exists
    app.register_blueprint(views, url_prefix = "/")  
    app.register_blueprint(auth, url_prefix = "/")
    
    # importing to here so during creation of app it initializes tables
    from .models import User
    
    #connecting app and database
    create_database(app)
    
    #user_loader helps current_user to identify who is authed
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('DMV/' + DB_NAME):
        with app.app_context():
            db.create_all()