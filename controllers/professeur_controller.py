from flask import Blueprint, render_template

professeur_bp = Blueprint("professeur", __name__)

@professeur_bp.route("/professeur")
def professeur():
    return render_template("professeur.html", titlepage="Professeur Page",stylefile="style")
