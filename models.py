from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    pdf_file = db.Column(db.String(255))  # file path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
