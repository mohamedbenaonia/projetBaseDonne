from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

matiere_bp = Blueprint("matiere_bp", __name__, url_prefix="/matiere")

@matiere_bp.route("/", methods=["GET"])
def get_matieres():
    db = get_db()
    matieres = db.execute("""
        SELECT matiere.*, filiere.nom as filiere_nom
        FROM matiere
        LEFT JOIN filiere ON matiere.filiere_id = filiere.id
    """).fetchall()
    return jsonify([dict(m) for m in matieres])

@matiere_bp.route("/", methods=["POST"])
def add_matiere():
    data = request.json
    db = get_db()
    db.execute(
        """INSERT INTO matiere (nom, code, description, coefficient, volume_horaire, filiere_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (data.get("nom"), data.get("code"), data.get("description"),
         data.get("coefficient", 1.0), data.get("volume_horaire"), data.get("filiere_id"))
    )
    db.commit()
    return jsonify({"message": "Matière créée avec succès"}), 201

@matiere_bp.route("/filiere/<int:filiere_id>")
def get_matieres_by_filiere(filiere_id):
    db = get_db()
    matieres = db.execute(
        "SELECT * FROM matiere WHERE filiere_id = ?", (filiere_id,)
    ).fetchall()
    return jsonify([dict(m) for m in matieres])

