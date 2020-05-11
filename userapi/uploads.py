from shopyoapi.init import fake
from app import app
from modules.auth.models import User

teachers = [(fake.name(), fake.email(), 'pass') for i in range(10)]
students = [(fake.name(), fake.email(), 'pass') for i in range(40)]

def upload_teachers():
    print('Adding Teachers ...')
    with app.app_context():
        for teacher in teachers:
            name = teacher[0]
            email = teacher[1]
            password = teacher[2]
            to_add_teacher = User(
                name=name,
                email=email,
                role='teacher'
                )
            to_add_teacher.set_hash(password)
            to_add_teacher.insert()
            print('[x] Added', teacher)

def upload_students():
    print('Adding Students ...')
    with app.app_context():
        for student in students:
            name = student[0]
            email = student[1]
            password = student[2]
            to_add_student = User(
                name=name,
                email=email,
                role='student'
                )
            to_add_student.set_hash(password)
            to_add_student.insert()
            print('[x] Added', student)


def upload_all():
    upload_teachers()
    upload_students()