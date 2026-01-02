from flask import Blueprint, request, jsonify, render_template
from database.db import get_db

absence_bp = Blueprint("absence_bp", __name__, url_prefix="/absence")

# Ajouter une absence
@absence_bp.route("/", methods=["POST"])
def add_absence():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO absence (id_etudiant, id_cours, id_professeur, date_absence) VALUES (?, ?, ?, ?)",
               (data["id_etudiant"], data["id_cours"], data.get("id_professeur"), data["date_absence"]))
    db.commit()
    return jsonify({"message": "Absence ajoutée"}), 201

# Voir absences d'un étudiant
@absence_bp.route("/etudiant/<int:id_etudiant>")
def absences_etudiant(id_etudiant):
    db = get_db()
    rows = db.execute(
        "SELECT absence.id, cours.nom as cours, absence.date_absence "
        "FROM absence JOIN cours ON absence.id_cours = cours.id "
        "WHERE id_etudiant = ?", (id_etudiant,)
    ).fetchall()
    return render_template("absence_etudiant.html", id_etudiant=id_etudiant)
