from flask import Blueprint, request
from controllers.user_controller import user_controller

user_blueprint = Blueprint("user", __name__)
user_controllerObj = user_controller()

@user_blueprint.route("/signup", methods=["POST"])
def signup():
    return user_controllerObj.signup(request)

@user_blueprint.route("/login", methods=["POST"])
def login():
    return user_controllerObj.login(request)