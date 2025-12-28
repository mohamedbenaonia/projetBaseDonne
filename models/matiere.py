from database.db import db

class Matiere(db.Model):
    __tablename__ = "matiere"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
