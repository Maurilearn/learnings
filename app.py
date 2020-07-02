import importlib
import os

from flask import Flask, redirect, send_from_directory
from flask import url_for
import json
from shopyoapi.init import db
from shopyoapi.init import login_manager
#from shopyoapi.init import ma

from shopyoapi.init import photos
from shopyoapi.init import docs
from shopyoapi.init import homeworksubmits
from shopyoapi.init import alldocs

from .config import app_config
from flask_wtf.csrf import CSRFProtect
from modules.auth.models import User
from flask_uploads import UploadSet, configure_uploads, IMAGES

base_path = os.path.dirname(os.path.abspath(__file__))

def create_app(config_name):
    app = Flask(__name__)
    configuration = app_config[config_name]
    app.config.from_object(configuration)

    db.init_app(app)
    #ma.init_app(app)
    csrf = CSRFProtect(app)
    
    configure_uploads(app, photos)
    configure_uploads(app, docs)
    configure_uploads(app, homeworksubmits)
    configure_uploads(app, alldocs)

    login_manager.init_app(app)
    login_manager.login_view = configuration.LOGIN_VIEW
    login_manager.login_message = configuration.LOGIN_MESSAGE

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    for module in os.listdir(os.path.join(base_path, "modules")):
        if module.startswith("__"):
            continue
        mod = importlib.import_module("modules.{}.view".format(module))
        app.register_blueprint(getattr(mod, "{}_blueprint".format(module)))


    @app.route("/")
    def index():
        return redirect(url_for('auth.login'))

    return app


with open(os.path.join(base_path, 'config.json')) as f:
    json_info = json.load(f)

app = create_app(json_info["environment"])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
