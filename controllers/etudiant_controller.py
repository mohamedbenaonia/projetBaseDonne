from flask import Blueprint, render_template
from models.etudiant import Etudiant  # ← importer le modèle
from database.db import db

etudiant_bp = Blueprint("etudiant", __name__, url_prefix="/etudiant")

@etudiant_bp.route("/")
def etudiant_home():
    etudiants = Etudiant.query.all()  # utilise le modèle
    return render_template("etudiant.html", titlepage="Page Étudiant", stylefile="style", etudiants=etudiants)
