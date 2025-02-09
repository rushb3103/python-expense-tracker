from flask import Blueprint, request, render_template, render_template_string
from controllers.user_controller import user_controller
from libraries.functions import functions

user_blueprint = Blueprint("user", __name__)
user_controllerObj = user_controller()
functionsObj = functions()

@user_blueprint.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        return user_controllerObj.signup(request)
    elif request.method == "GET":
        return render_template("/user/signup.html")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    # print("A")
    # print(request.method)
    if request.method == 'GET':
        # print("G")
        return render_template('/user/login.html')
        # return 'OK'
    elif request.method == 'POST':
        # print("P")
        return user_controllerObj.login(request)
    
@user_blueprint.route("/home", methods=["GET", "POST"])
@functions.token_required
def home(user=0):
    print(user)
    if request.method == 'GET':
        # print("G")
        # return render_template('/user/login.html')
        return "<p>Hello, I am Rushit !!</p>"
        # return 'OK'
    elif request.method == 'POST':
        # print("P")
        return user_controllerObj.home(request)


# @user_blueprint.route("/login", methods=["POST"])
# def login():
#     return user_controllerObj.login(request)
