from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
from sqlalchemy.sql.functions import user
import urllib
import traceback


db = SQLAlchemy()

def create_app():
    
    # Configure Database URI: 
    params = urllib.parse.quote_plus(
        'Driver=%s;' % 'ODBC Driver 17 for SQL Server' +
        'Server=tcp:%s,1433;' % 'updoc.database.windows.net' +
        'Database=%s;' % 'UpDocSQL' +
        'Uid=%s;' % 'amir' +
        'Pwd={%s};' % 'amk@1912' +
        'Encrypt=yes;' +
        'TrustServerCertificate=no;' +
        'Connection Timeout=30;')

    # Initialize application with URI for Azure DB
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dfvovniv bfuo3bfui3fih'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Student, Documents

    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Student.query.get(int(id))

    return app
