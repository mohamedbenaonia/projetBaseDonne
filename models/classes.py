from database.db import db

class Classe(db.Model):
    __tablename__ = "classe"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    niveau = db.Column(db.String(30))
