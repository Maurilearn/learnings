
from flask import Blueprint
school_blueprint = Blueprint(
    "school",
    __name__,
    url_prefix='/school',
    template_folder="templates",
)


@school_blueprint.route("/")
def index():
    return 'index page'
