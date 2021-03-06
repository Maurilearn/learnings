from werkzeug.security import generate_password_hash, check_password_hash
from shopyoapi.init import db
from flask_login import UserMixin

from modules.course.models import Course
from modules.lightcourse.models import LightCourse
from modules.course.models import QuizHistory

course_subs = db.Table('course_subs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)
light_course_subs = db.Table('light_course_subs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('light_course_id', db.Integer, db.ForeignKey('light_courses.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(128))
    name = db.Column(db.String(120))
    role = db.Column(db.String(120))
    pass_changed = db.Column(db.Boolean, default=False)

    courses = db.relationship("Course",
        secondary=course_subs, 
        cascade = "all, delete")# !subs- teacher, students
    light_courses = db.relationship("LightCourse",
        secondary=light_course_subs, 
        cascade = "all, delete")# !subs- teacher, students

    quiz_histories = db.relationship('QuizHistory', backref='person', lazy=True,
        cascade="all, delete, delete-orphan")

    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'))

    def set_hash(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_hash(self, password):
        return check_password_hash(self.password, password)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()