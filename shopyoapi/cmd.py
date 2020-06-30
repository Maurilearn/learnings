import os
import shutil
import sys
import subprocess
import json
import importlib

from app import app
from shopyoapi.init import db
from shopyoapi.utils import trycopytree
from shopyoapi.utils import trycopy
from shopyoapi.utils import trymkdir
from shopyoapi.utils import trymkfile
from shopyoapi.uploads import add_admin
from shopyoapi.uploads import add_setting

#from shopyoapi.uploads import add_setting


def new_project(path, newfoldername):
    newfoldername = newfoldername.strip('/').strip('\\')
    print("creating new project {}".format(newfoldername))

    base_path = path + "/" + newfoldername
    trymkdir(base_path)
    print("created dir {} in {}".format(newfoldername, path))

    trycopytree("./static", base_path + "/static")
    trycopytree("./tests", base_path + "/tests")
    trycopytree("./modules/base", base_path + "/modules/base")
    trycopytree("./modules/admin", base_path + "/modules/admin")
    trycopytree("./modules/login", base_path + "/modules/login")
    trycopytree("./shopyoapi", base_path + "/shopyoapi")

    trycopy("app.py", base_path + "/app.py")
    trycopy("config.json", base_path + "/config.json")
    trycopy("config.py", base_path + "/config.py")
    trycopy("manage.py", base_path + "/manage.py")
    trycopy("base_test.py", base_path + "/base_test.py")


def clean():
    if os.path.exists("test.db"):
        os.remove("test.db")
        print("test.db successfully deleted")
    else:
        print("test.db doesn't exist")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print("__pycache__ successfully deleted")
    else:
        print("__pycache__ doesn't exist")

    while 1:
        answer = input(
            'Still want to continue? This will re-initialise your whole app\n'
            'y/n ?\n'
            '> ')
        answer = answer.casefold().strip()
        if answer in ['y', 'n']:
            if answer == 'n':
                print('Setup abortion confirmed, exiting ...')
                sys.exit()
            elif answer == 'y':
                break
        else:
            print('Could not understand answer. Exiting ...')
            sys.exit()

    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
        print("[x] migrations folder successfully deleted")
    else:
        print("[ ] migrations folder doesn't exist")

    from app import app
    with app.test_request_context():
        db.drop_all()
        db.engine.execute('DROP TABLE IF EXISTS alembic_version;')
        print("[x] all tables dropped")
    
'''
    
    while 1:
        answer = input(
            'Still want to continue? This will re-initialise your whole app\n'
            'y/n ?\n'
            '> ')
        answer = answer.casefold().strip()
        if answer in ['y', 'n']:
            if answer == 'n':
                print('Setup abortion confirmed, exiting ...')
                sys.exit()
            elif answer == 'y':
                break
        else:
            print('Could not understand answer. Exiting ...')
            sys.exit()
            '''

def initialise():
    print('initialising ...')
    print(
        'Warning!\n'
        'Make sure your database exists. The code will only create '
        'tables for you'
        )
    print("Creating Tables")
    print("#######################")
    with open("config.json", "r") as config:
        config = json.load(config)
    
    subprocess.run(
        [sys.executable, "manage.py", "db", "init"], stdout=subprocess.PIPE
    )
    print("Migrating")
    print("#######################")
    subprocess.run(
        [sys.executable, "manage.py", "db", "migrate"], stdout=subprocess.PIPE
    )
    subprocess.run(
        [sys.executable, "manage.py", "db", "upgrade"], stdout=subprocess.PIPE
    )

    print("Initialising User")
    print("#######################")
    for admin_config in config['admins']:
        add_admin(
            admin_config["name"],
            admin_config["email"],
            admin_config["password"]
        )

    print("Applying settings")
    print("#######################")
    subprocess.run(
        [sys.executable, "manage.py", "applysettings"], stdout=subprocess.PIPE
    )

    print("Done!")

def create_module(modulename):
    print('creating module: {}'.format(modulename))
    base_path = 'modules/' + modulename
    trymkdir(base_path)
    trymkdir(base_path+'/templates')
    trymkdir(base_path+'/templates/'+modulename)
    view_content = '''
from flask import Blueprint
{0}_blueprint = Blueprint(
    "{0}",
    __name__,
    url_prefix='/{0}',
    template_folder="templates",
)


@{0}_blueprint.route("/")
def index():
    pass
'''.format(modulename)
    trymkfile(base_path+'/'+'view.py', view_content)
    trymkfile(base_path+'/'+'forms.py', '')
    trymkfile(base_path+'/'+'models.py', '')


def apply_settings():
    with open("config.json", "r") as config:
        config = json.load(config)
    add_setting('school_name', config['school']['name'])
    add_setting('contact_mail', config['school']['contact_mail'])
    add_setting('logo', None)



