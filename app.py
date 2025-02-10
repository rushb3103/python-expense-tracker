













from libraries.db import db
from route.user import user_blueprint
from route.transactions import transaction_blueprint
from flask_cors import CORS

from flask import Flask

app = Flask(__name__)
dbObj = db()
app.static_folder = 'static'
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, I am Rushit !!</p>"

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(transaction_blueprint, url_prefix="/transaction")

if  __name__ ==  '__main__':
    app.run(debug=True)


