from flask import Blueprint
from app.controllers import mainController

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

@api_blueprint.route("/test")
def test():
    return mainController.test() #!need to put in a session