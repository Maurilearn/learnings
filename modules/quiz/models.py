from shopyoapi.init import db


class Quiz(db.Model):
    __tablename__ = 'quizes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    question = db.Column(db.String(100))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'),
        nullable=False)
    # https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
    answers = db.relationship('Answer', backref='quiz', lazy=True,
        cascade="all, delete, delete-orphan", order_by='func.random()')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    string = db.Column(db.String(100))
    correct = db.Column(db.Boolean)
    quizz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()