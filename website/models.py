from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Documents(db.Model, UserMixin):
    Doc_id = db.Column(db.Integer, primary_key=True)
    Document_Uploaded = db.Column(db.String(1000))
    uploaded_on = db.Column(db.DateTime(timezone=True), default=func.now())
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    filename = db.Column(db.String(1000))
    #documents = db.relationship('Documents')

class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Email_Id = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    student_name = db.Column(db.String(150))
    #documents = db.relationship('Documents')


