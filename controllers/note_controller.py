from flask import Blueprint, request, jsonify, render_template
from database.db import get_db

note_bp = Blueprint("note_bp", __name__, url_prefix="/note")

# Ajouter une note
@note_bp.route("/", methods=["POST"])
def add_note():
    data = request.json
    db = get_db()
    db.execute("INSERT INTO note (id_etudiant, id_cours, id_professeur, valeur, commentaire) VALUES (?, ?, ?, ?, ?)",
               (data["id_etudiant"], data["id_cours"], data.get("id_professeur"), data["valeur"], data.get("commentaire", "")))
    db.commit()
    return jsonify({"message": "Note ajoutée"}), 201

# Voir notes d'un étudiant
@note_bp.route("/etudiant/<int:id_etudiant>")
def notes_etudiant(id_etudiant):
    db = get_db()
    rows = db.execute(
        "SELECT note.id, cours.nom as cours, note.valeur "
        "FROM note JOIN cours ON note.id_cours = cours.id "
        "WHERE id_etudiant = ?", (id_etudiant,)
    ).fetchall()
    return render_template("note_etudiant.html", id_etudiant=id_etudiant)
