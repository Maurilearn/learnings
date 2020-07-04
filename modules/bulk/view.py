
from flask import Blueprint
bulk_blueprint = Blueprint(
    "bulk",
    __name__,
    url_prefix='/bulk',
    template_folder="templates",
)


@bulk_blueprint.route("/")
def index():
    pass
