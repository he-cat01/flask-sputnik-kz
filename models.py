from app import db
from datetime import datetime

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String)
    title = db.Column(db.String)
    link = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.now())

