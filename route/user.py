from flask import Blueprint, request, render_template, render_template_string
from controllers.user_controller import user_controller

user_blueprint = Blueprint("user", __name__)
user_controllerObj = user_controller()

@user_blueprint.route("/signup", methods=["POST"])
def signup():
    return user_controllerObj.signup(request)

@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    print("A")
    print(request.method)
    if request.method == 'GET':
        print("G")
        return render_template('/user/login.html')
        # return 'OK'
    elif request.method == 'POST':
        print("P")
        return user_controllerObj.login(request)


# @user_blueprint.route("/login", methods=["POST"])
# def login():
#     return user_controllerObj.login(request)
