
import sys
import traceback
import os

import pandas as pd
from flask import jsonify, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from models import db, Expense
from forms import UploadFileForm
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db



app = Flask(__name__)
app.config.from_object(Config)

# Attach SQLAlchemy to this app
db.init_app(app)
csrf = CSRFProtect(app)

import logging
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

logging.basicConfig(
    filename="./flask.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
)
app.logger.addHandler(logging.FileHandler("./flask.log"))
app.logger.setLevel(logging.DEBUG)

@app.route("/")
def hello_world():
    return "<p>Hello, I am Rushit !!</p>"



@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadFileForm()

    # Normal GET → render page
    if request.method == "GET":
        return render_template("upload.html", form=form)

    # Handle POST
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Parse CSV
        df = pd.read_csv(filepath, skiprows=22, sep='~', error_bad_lines=False)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df = df[df['transaction_type'].isin(["Domestic", "International"])]

        transactions = []
        for row in df.itertuples():
            tx = {
                "date": pd.to_datetime(row.date, errors="coerce").strftime("%Y-%m-%d %H:%M:%S"),
                "description": str(row.description),
                "amount": float(str(row.amt).replace(",", "")),
                "transaction_type": "Debit" if getattr(row, "_6", "").strip() == "" else "Credit",
                "category": "Uncategorized",
                "filepath": filepath,
            }
            transactions.append(tx)

            # Also save in DB
            expense = Expense(
                transaction_date=tx["date"],
                description=tx["description"],
                amount=tx["amount"],
                transaction_type=tx["transaction_type"],
                category=tx["category"],
                filepath=tx["filepath"]
            )
            db.session.add(expense)

        db.session.commit()

        # ✅ Always return JSON for frontend
        return {
            "status": "success",
            "rows": len(transactions),
            "transactions": transactions
        }

    # Validation failed
    return {"status": "error", "message": "Invalid form"}, 400

@app.route("/debug")
def debug():
    import os
    app.logger.info("Debug route hit!")
    return str({k: os.environ[k] for k in ("SCRIPT_NAME","PATH_INFO","REQUEST_URI") if k in os.environ})

# @app.errorhandler(Exception)
# def handle_exception(e):
#     # app.logger.exception("Unhandled Exception: %s", e)
#     return "Internal Server Error – check logs", 500


if  __name__ ==  '__main__':
    from models import db
    with app.app_context():
        db.create_all()
    app.run(debug=True)
