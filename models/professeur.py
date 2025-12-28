from database.db import db

class Professeur(db.Model):
    __tablename__ = "professeur"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
