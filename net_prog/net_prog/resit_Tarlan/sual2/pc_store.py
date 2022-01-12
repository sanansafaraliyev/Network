from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import flask_sqlalchemy


app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///final.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)


class Students(db.Model):
    stud_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Student (Name = {name}, Surname = {surname}, Email = {email})>"


class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Course {title}>"

class Marks(db.Model):
    mark_id = db.Column(db.Integer, primary_key=True)
    stud_id = db.Column(db.Integer, db.ForeignKey("Students.stud_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("Courses.course_id"), nullable=False)


db.create_all()


student_post_args = reqparse.RequestParser()
student_post_args.add_argument("name", type=str, help ="Name of the student", required=True)
student_post_args.add_argument("surname", type=str, help ="Surname of the student", required=True)
student_post_args.add_argument("email", type=str, help ="Email of the student", required=True)

course_post_args = reqparse.RequestParser()
course_post_args.add_argument("title", type=str, help="Title of the course", required=True)

mark_post_args = reqparse.RequestParser()
mark_post_args.add_argument("stud_id", type=int, help="Student ID", required=True)
mark_post_args.add_argument("course_id", type=int, help="Course ID", required=True)


resource_fields_students = {
    "stud_id": fields.integer,
    "name": fields.String,
    "surname": fields.String,
    "email": fields.String
}

resource_fields_courses{
    "course_id": fields.Integer,
    "title": fields.String
}

resource_fields_marks{
    "mark_id": fields.Integer,
    "stud_id": fields.Integer,
    "course_id": fields.Integer
}




