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
    
@user_blueprint.route("/home", methods=["POST"])
@functions.token_required
def get_home(user_id=0):
    print(user_id)
    if request.method == 'GET':
        context = {"title" : "HOME"}
        return render_template('/user/home.html', **context)
        return user_controllerObj.home(request, user_id)
        # return 'OK'
    elif request.method == 'POST':
        # print("P")
        return user_controllerObj.home(request, user_id)
@user_blueprint.route("/home", methods=["GET"])
def post_home(user_id=0):
    print(user_id)
    if request.method == 'GET':
        return render_template('/user/home.html')
        # return user_controllerObj.home(request, user_id)
        # return 'OK'
    elif request.method == 'POST':
        # print("P")
        return user_controllerObj.home(request, user_id)
    
@user_blueprint.route("/dashboard", methods=["GET"])
@functions.token_required
def dashboard(user_id=0):
    print(user_id)
    if request.method == 'GET':
        # return render_template('/user/home.html')
        return user_controllerObj.home(request, user_id)
        # return 'OK'



# @user_blueprint.route("/login", methods=["POST"])
# def login():
#     return user_controllerObj.login(request)
