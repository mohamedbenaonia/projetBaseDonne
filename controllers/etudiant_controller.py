from flask import Blueprint, render_template
from database.db import get_db

etudiant_bp = Blueprint("etudiant", __name__, url_prefix="/etudiant")

@etudiant_bp.route("/")
def etudiant_home():
    db = get_db()
    etudiants = db.execute(
        "SELECT * FROM etudiant"
    ).fetchall()

    return render_template(
        "etudiant.html",
        titlepage="Page Étudiant",
        stylefile="style",
        etudiants=etudiants
    )
