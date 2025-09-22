
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
    try:
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            
            df = pd.read_csv(filepath, skiprows=22, sep='~', error_bad_lines=False)
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            df = df[df['transaction_type'].isin(["Domestic", "International"])]
            
            # return {"message": "File processed", "rows": len(df)}
            transaction_list = []
            
            for row in df.itertuples():
                transaction_json = {
                    "date": pd.to_datetime(row.date, errors="coerce"),
                    "description": str(row.description),
                    "amount": float(str(row.amt).replace(",", "")),
                    "transaction_type": "Debit" if getattr(row, "_6", "").strip() == "" else "Credit",
                    "category": "Uncategorized",
                    "filepath": filepath
                }
                try:
                    expense = Expense(
                        transaction_date=transaction_json["date"],
                        description=transaction_json["description"],
                        amount=transaction_json["amount"],
                        transaction_type=transaction_json["transaction_type"],
                        category=transaction_json["category"],
                        filepath=transaction_json["filepath"]
                    )
                    db.session.add(expense)
                    transaction_list.append(transaction_json)
                except Exception:
                    print("Row failed:", row, file=sys.stderr)
                    print(traceback.format_exc(), file=sys.stderr)
                    continue

            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                print(traceback.format_exc(), file=sys.stderr)
                return {"error": "DB commit failed", "trace": traceback.format_exc()}, 500
            
                        # ✅ If AJAX upload, return JSON for charts
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({
                    "status": "success",
                    "rows": len(transaction_list),
                    "transactions": transaction_list
                })
    
        
            flash("File uploaded and parsed successfully!")
            return redirect("/upload")

        return render_template("upload.html", form=form)
    except Exception as e:
        error = traceback.format_exc()
        print(error)
        app.logger.exception("Error in upload route: %s", e)
        flash("An error occurred while processing the file.")
        return {"error": error}, 500
        # return redirect(url_for("upload"))

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
