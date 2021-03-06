from shopyoapi.init import db
from datetime import datetime

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    courses = db.relationship('Course', backref='grade', lazy=True,
        cascade="all, delete, delete-orphan")
    light_courses = db.relationship('LightCourse', backref='grade', lazy=True,
        cascade="all, delete, delete-orphan")
    students = db.relationship('User', backref='grade', lazy=True,
        cascade="all, delete, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return self.name


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.now())
    submitted = db.Column(db.Boolean, default=False)
    teacher_id = db.Column(db.Integer, 
        nullable=False)
    sections = db.relationship('Section', backref='course', lazy=True,
        cascade="all, delete, delete-orphan")
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



learningpath_subs = db.Table('learningpath_subs',
    db.Column('learningpath_id', db.Integer, db.ForeignKey('learning_paths.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)
class LearningPath(db.Model):
    __tablename__ = 'learning_paths'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    courses = db.relationship("Course",
        secondary=learningpath_subs, 
        cascade = "all, delete")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.now())
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
        nullable=False)
    quizzes = db.relationship('Quiz', backref='section', lazy=True,
        cascade="all, delete, delete-orphan")
    quiz_histories = db.relationship('QuizHistory', backref='section', lazy=True,
        cascade="all, delete, delete-orphan")
    sub_sections = db.relationship('SubSection', backref='section', lazy=True,
        cascade="all, delete, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class SubSection(db.Model):
    __tablename__ = 'sub_sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.now())
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'),
        nullable=False)
    resources = db.relationship('Resource', backref='sub_section', lazy=True,
        cascade="all, delete, delete-orphan")
    homeworks = db.relationship('Homework', backref='sub_section', lazy=True,
        cascade="all, delete, delete-orphan")
    homework_submissions = db.relationship('HomeworkSubmission', backref='sub_section', lazy=True,
        cascade="all, delete, delete-orphan")
    homework_evaluations = db.relationship('HomeworkEvaluation', backref='sub_section', lazy=True,
        cascade="all, delete, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Homework(db.Model):
    __tablename__ = 'homeworks'
    id = db.Column(db.Integer, primary_key=True)
    subsection_id = db.Column(db.Integer, db.ForeignKey('sub_sections.id'),
        nullable=False)
    filename = db.Column(db.String(100)) # uploads/homework/

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class HomeworkSubmission(db.Model):
    __tablename__ = 'homework_submissions'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    subsection_id = db.Column(db.Integer, db.ForeignKey('sub_sections.id'),
        nullable=False)
    filename = db.Column(db.String(100))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class HomeworkEvaluation(db.Model):
    __tablename__ = 'homework_evaluations'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    subsection_id = db.Column(db.Integer, db.ForeignKey('sub_sections.id'),
        nullable=False)
    notes = db.Column(db.String(100))
    filename = db.Column(db.String(100))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), default='text')
    filename = db.Column(db.String(100))
    path = db.Column(db.String(100))
    text = db.Column(db.Text)
    sub_section_id = db.Column(db.Integer, db.ForeignKey('sub_sections.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class QuizHistory(db.Model):
    '''
    section quiz completed
    '''
    __tablename__ = 'quiz_histories'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'),
        nullable=False)
    completed = db.Column(db.Boolean, default=True,
        nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ChapterHistory(db.Model):
    __tablename__ = 'section_histories'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    subsection_id = db.Column(db.Integer, db.ForeignKey('sub_sections.id'),
        nullable=False)
    completed = db.Column(db.Boolean, default=True,
        nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class CertificateRequest(db.Model):
    __tablename__ = 'certificate_requests'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'),
        nullable=False)
    date_given = db.Column(db.DateTime, default=datetime.now())
    filename = db.Column(db.String(100))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

