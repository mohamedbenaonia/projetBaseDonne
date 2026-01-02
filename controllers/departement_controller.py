from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

departement_bp = Blueprint("departement_bp", __name__, url_prefix="/departement")

@departement_bp.route("/", methods=["GET"])
def get_departements():
    db = get_db()
    departements = db.execute("""
        SELECT departement.*, professeur.nom as chef_nom, professeur.prenom as chef_prenom
        FROM departement
        LEFT JOIN professeur ON departement.chef_departement_id = professeur.id
    """).fetchall()
    return jsonify([dict(d) for d in departements])

@departement_bp.route("/", methods=["POST"])
def add_departement():
    data = request.json
    db = get_db()
    db.execute(
        """INSERT INTO departement (nom, description, chef_departement_id)
           VALUES (?, ?, ?)""",
        (data.get("nom"), data.get("description"), data.get("chef_departement_id"))
    )
    db.commit()
    return jsonify({"message": "Département créé avec succès"}), 201

@departement_bp.route("/<int:departement_id>/professeurs")
def get_professeurs_departement(departement_id):
    db = get_db()
    professeurs = db.execute(
        "SELECT * FROM professeur WHERE departement_id = ?", (departement_id,)
    ).fetchall()
    return jsonify([dict(p) for p in professeurs])

