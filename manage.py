import sys

from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager

from shopyoapi.init import db
from app import app

from shopyoapi.cmd import new_project
from shopyoapi.cmd import clean
from shopyoapi.cmd import initialise
from shopyoapi.cmd import create_module
from shopyoapi.cmd import apply_settings
from shopyoapi.database import autoload_models
from userapi.uploads import upload_all


migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


def runserver():
    app.run()


def rundebug(port=5000):
    print('LEARNING MANAGEMENT SYSTEM')
    app.run(debug=True, host="0.0.0.0", port=port)


def custom_commands(args):
    # non migration commands
    if args[1] != "db":
        if args[1] == "initialise":
            # auto import models
            autoload_models()
            initialise()
        elif args[1] == "clean":
            clean()
        elif args[1] == "runserver":
            runserver()
        elif args[1] == "rundebug":
            if len(args) == 2+1:
                rundebug(port=int(args[2]))
            else:
                rundebug()
        elif args[1] == "test":
            print("test ok")
        elif args[1] == "new" and args[2] and args[3]:
            # new <path> <folder name>
            new_project(args[2], args[3])
        elif args[1] == 'startapp' and args[2]:
            create_module(args[2])
        elif args[1] == 'populate':
            upload_all()
        elif args[1] == 'applysettings':
            apply_settings()
        sys.exit()
    elif args[1] == "db":
        autoload_models()


if __name__ == "__main__":
    custom_commands(sys.argv)
    manager.run()
