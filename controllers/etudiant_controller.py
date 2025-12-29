from flask import Blueprint, render_template

# Le nom doit être exactement etudiant_bp
etudiant_bp = Blueprint("etudiant", __name__)

@etudiant_bp.route("/etudiant")
def etudiant():
    return render_template("etudiant.html", titlepage="Etudiant Page",stylefile="style")
