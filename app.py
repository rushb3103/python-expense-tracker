













from libraries.db import db
from controllers.user_controller import user_controller

from flask import Flask

app = Flask(__name__)
dbObj = db()

@app.route("/")
def hello_world():
    return "<p>Hello, I am Rushit !!</p>"

@app.route("/signup")
def signup():
    user_controllerObj = user_controller()
    return user_controllerObj.signup()


if  __name__ ==  '__main__':
	app.run(debug=True)


