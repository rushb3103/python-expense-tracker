from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadFileForm(FlaskForm):
    file = FileField("Upload File", validators=[DataRequired()])
    submit = SubmitField("Upload")
