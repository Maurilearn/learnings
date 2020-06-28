from shopyoapi.init import db
from datetime import datetime

class LightQuiz(db.Model):
    __tablename__ = 'light_quizes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    question = db.Column(db.String(100))
    course_id = db.Column(db.Integer, db.ForeignKey('light_courses.id'),
        nullable=False)
    # https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
    answers = db.relationship('LightAnswer', backref='quiz', lazy=True,
        cascade="all, delete, delete-orphan", order_by='func.random()')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class LightAnswer(db.Model):
    __tablename__ = 'light_answers'
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String(100))
    correct = db.Column(db.Boolean)
    quizz_id = db.Column(db.Integer, db.ForeignKey('light_quizes.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class LightCourse(db.Model):
    __tablename__ = 'light_courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.now())
    submitted = db.Column(db.Boolean, default=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'),
        nullable=False)
    chapters = db.relationship('LightChapter', backref='course', lazy=True,
        cascade="all, delete, delete-orphan")
    quizzes = db.relationship('LightQuiz', backref='course', lazy=True,
        cascade="all, delete, delete-orphan")
    light_certificate = db.relationship('LightCertificate', backref='course', lazy=True,
        cascade="all, delete, delete-orphan", uselist=False)
    light_certificate_requests = db.relationship('LightCertificateRequest', backref='course', lazy=True,
        cascade="all, delete, delete-orphan")
    light_quiz_histories = db.relationship('LightQuizHistory', backref='course', lazy=True,
        cascade="all, delete, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class LightChapter(db.Model):
    __tablename__ = 'light_chapters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.now())
    light_course_id = db.Column(db.Integer, db.ForeignKey('light_courses.id'),
        nullable=False)
    resources = db.relationship('LightResource', backref='chapter', lazy=True,
        cascade="all, delete, delete-orphan")
    homeworks = db.relationship('LightHomework', backref='chapter', lazy=True,
        cascade="all, delete, delete-orphan")
    homework_submissions = db.relationship('LightHomeworkSubmission', backref='chapter', lazy=True,
        cascade="all, delete, delete-orphan")
    homework_evaluations = db.relationship('LightHomeworkEvaluation', backref='chapter', lazy=True,
        cascade="all, delete, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class LightHomework(db.Model):
    __tablename__ = 'light_homeworks'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('light_chapters.id'),
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


class LightHomeworkSubmission(db.Model):
    __tablename__ = 'light_homework_submissions'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('light_chapters.id'),
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


class LightHomeworkEvaluation(db.Model):
    __tablename__ = 'light_homework_evaluations'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('light_chapters.id'),
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


class LightResource(db.Model):
    __tablename__ = 'light_resources'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), default='text')
    filename = db.Column(db.String(100))
    path = db.Column(db.String(100))
    text = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey('light_chapters.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class LightQuizHistory(db.Model):
    '''
    chapter quiz completed
    '''
    __tablename__ = 'light_quiz_histories'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    light_course_id = db.Column(db.Integer, db.ForeignKey('light_courses.id'),
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


class LightChapterHistory(db.Model):
    __tablename__ = 'light_section_histories'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('light_chapters.id'),
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


class LightCertificateRequest(db.Model):
    __tablename__ = 'light_certificate_requests'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('light_courses.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class LightCertificate(db.Model):
    __tablename__ = 'light_certificates'
    id = db.Column(db.Integer, primary_key=True)
    course_taker_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('light_courses.id'),
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