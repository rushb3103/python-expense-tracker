from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadPDFForm(FlaskForm):
    pdf_file = FileField("Upload PDF", validators=[DataRequired()])
    submit = SubmitField("Upload")
