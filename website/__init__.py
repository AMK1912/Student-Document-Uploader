from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
from sqlalchemy.sql.functions import user
import urllib
import traceback


db = SQLAlchemy()

def create_app():

    try:
        # using the above logic I just did the following
        #params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=LAPTOP-O72FEI27\SQLEXPRESS;DATABASE=Students;Trusted_Connection=yes;')
        #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params 
        #params = urllib.parse.quote_plus('DRIVER={SQL Server};Server=tcp:updoc.database.windows.net,1433;DATABASE=UpDocSQL;Trusted_Connection=yes;')
        #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params 
        #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://amir:amk@1912@tcp:updoc.database.windows.net:1433/UpDocSQL"
        #app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://LAPTOP-O72FEI27\SQLEXPRESS/Students?driver=SQL+Server?trusted_connection=yes"
        #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://user:pwd@server/database?driver=SQL+Server"
        #app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://LAPTOP-O72FEI27\SQLEXPRESS/Students?driver=SQL+Server?trusted_connection=yes"
        #server = 'updoc.database.windows.net'
        #database = 'UpDocSQL'
        #username = 'amir'
        #password = 'amk@1912'   
        #driver= 'ODBC Driver 17 for SQL Server'

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

    except Exception as e:
        print('A problem has occurred from the Problematic code: ', e)

    @login_manager.user_loader
    def load_user(Id):
        try:
            return Student.query.get(int(Id))

        except Exception as e: 
            traceback.print_exc()
    return app
