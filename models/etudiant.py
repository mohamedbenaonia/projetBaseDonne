from database.db import db

class Etudiant(db.Model):
    __tablename__ = "etudiant"  # nom de la table

    id = db.Column(db.Integer, primary_key=True)  # clé primaire
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
