
import traceback
import os

import pandas as pd
from flask import render_template, request, redirect, url_for, flash
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

logging.basicConfig(
    filename="./flask.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
)


@app.route("/")
def hello_world():
    return "<p>Hello, I am Rushit !!</p>"




@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        df = pd.read_csv(filepath, skiprows=22, sep='~', error_bad_lines=False)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df = df[df['transaction_type'].isin(["Domestic", "International"])]
        
        for row in df.itertuples():
            try:
                expense = Expense(
                    transaction_date=row.date,
                    description=row.description,
                    amount=float(row.amt.replace(",", "")),
                    transaction_type="Debit" if row._6.strip() == "" else "Credit",
                    category="Uncategorized",
                    filepath=filepath
                )
                db.session.add(expense)
            except Exception as e:
                print(traceback.format_exc())
                continue
            
        db.session.commit()

        flash("File uploaded and parsed successfully!")
        return redirect(url_for("upload"))

    return render_template("upload.html", form=form)


# if  __name__ ==  '__main__':
#     from models import db
#     with app.app_context():
#         db.create_all()
#     app.run()
