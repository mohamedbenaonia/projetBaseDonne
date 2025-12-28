from database.db import db

class Administrateur(db.Model):
    __tablename__ = "administrateur"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
