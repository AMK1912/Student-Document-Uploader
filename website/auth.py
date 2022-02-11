from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
from .models import Student, Documents
from flask_login import login_user, login_required, logout_user, current_user
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os
from datetime import date

today = date.today()
auth = Blueprint('auth',__name__)

#app.config.from_pyfile('Config.py')
#account = app.config['ACCOUNT_NAME']   # Azure account name
#key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = "DefaultEndpointsProtocol=https;AccountName=updocst;AccountKey=YopaE7MD6BkWhZcO5D0TTxM0EhZBbsG4pizVZ8pv0fDVqdZ+FJqMpNUsMjXJgEujhkWai3yqjdoWxi/EphudmA==;EndpointSuffix=core.windows.net"
container = "updocblob" # Container name
allowed_ext = set(['txt', 'pdf', 'png', 'jpg', 'jpeg']) # List of accepted extensions
max_length = 20 * 1024 * 1024 # Maximum size of the uploaded file

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in allowed_ext

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Student.query.filter_by(Email_Id=email, password=password).first()  
        if user:
            #if check_password_hash(user.password, password):
        
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
            
        else:
            flash('Either Email does not exist or Password is not correct, Please try again', category='error')
    
    return render_template("login.html", user=current_user)
 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        Email_Id = request.form.get('email')
        student_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Student.query.filter_by(Email_Id=Email_Id).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(Email_Id) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(student_name) < 2:
            flash('User name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:      
            #new_user = Student(Email_Id=Email_Id,student_name=student_name, password=generate_password_hash(password1, method='sha256')) 
            new_user = Student(Email_Id=Email_Id,student_name=student_name, password=password1) 
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        user=current_user
        if user!=None:
            studentid= user.get_id()
        img = request.files['file']
        if img and allowed_file(img.filename):
            filename = img.filename
            img.save(filename)
            blob_client = blob_service_client.get_blob_client(container = container, blob = filename)
            with open(filename, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    docurl=blob_client.url
                    #docurl="www.google.com"
                    new_document=Documents(student_id=studentid,Document_Uploaded=docurl,filename=filename)
                    db.session.add(new_document)
                    db.session.commit()
                    msg = "Upload Done ! "
                    flash(msg, category='success')
                except:
                    pass
            os.remove(filename)
    return render_template("UploadFiles.html", user=current_user)

@auth.route('/list')
def list():
    user=current_user
    if user!=None:
        studentid= user.get_id()
        documents = Documents.query.filter_by(student_id=studentid)  
        return render_template('List.html', title='Document Table',documents=documents,user=current_user)
