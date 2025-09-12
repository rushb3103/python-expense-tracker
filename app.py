















from flask import Flask

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# Attach SQLAlchemy to this app
db.init_app(app)
csrf = CSRFProtect(app)


@app.route("/")
def hello_world():
    return "<p>Hello, I am Rushit !!</p>"

import os
import pdfplumber
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from models import db, Expense
from forms import UploadPDFForm


@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadPDFForm()
    if form.validate_on_submit():
        file = form.pdf_file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Example PDF parsing (simple text scan)
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                # naive parse: split by lines
                for line in text.split("\n"):
                    if "INR" in line:  # crude filter for transactions
                        parts = line.split()
                        try:
                            expense = Expense(
                                transaction_date=parts[0],
                                description=" ".join(parts[1:-1]),
                                amount=float(parts[-1].replace(",", "")),
                                category="Uncategorized",
                                pdf_file=filename
                            )
                            db.session.add(expense)
                        except Exception as e:
                            continue
            db.session.commit()

        flash("PDF uploaded and parsed successfully!")
        return redirect(url_for("upload"))

    return render_template("upload.html", form=form)


if  __name__ ==  '__main__':
    from models import db
    with app.app_context():
        db.create_all()
    app.run()
