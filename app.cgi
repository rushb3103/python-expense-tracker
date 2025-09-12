#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from app import app

from models import db
with app.app_context():
    db.create_all()


CGIHandler().run(app)
