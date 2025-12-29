from flask import Blueprint, render_template
from models.professeur import Professeur
from database.db import db

professeur_bp = Blueprint("professeur", __name__, url_prefix="/professeur")

@professeur_bp.route("/")
def professeur_home():
    professeurs = Professeur.query.all()
    return render_template("professeur.html", titlepage="Page Professeur", stylefile="style", professeurs=professeurs)
