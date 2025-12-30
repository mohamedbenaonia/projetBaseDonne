from flask import Blueprint, render_template
from database.db import get_db

professeur_bp = Blueprint("professeur", __name__, url_prefix="/professeur")

@professeur_bp.route("/")
def professeur_home():
    db = get_db()
    professeurs = db.execute(
        "SELECT * FROM professeur"
    ).fetchall()

    return render_template(
        "professeur.html",
        titlepage="Page Professeur",
        stylefile="style",
        professeurs=professeurs
    )
