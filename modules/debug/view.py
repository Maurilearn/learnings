
from flask import Blueprint
debug_blueprint = Blueprint(
    "debug",
    __name__,
    url_prefix='/debug',
    template_folder="templates",
)


@debug_blueprint.route("/")
def index():
    pass
