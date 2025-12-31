from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

salle_bp = Blueprint("salle_bp", __name__, url_prefix="/salle")

@salle_bp.route("/", methods=["GET"])
def get_salles():
    db = get_db()
    salles = db.execute("SELECT * FROM salle ORDER BY numero").fetchall()
    return jsonify([dict(s) for s in salles])

@salle_bp.route("/", methods=["POST"])
def add_salle():
    data = request.json
    db = get_db()
    db.execute(
        """INSERT INTO salle (numero, nom, capacite, type_salle, equipements, batiment, etage)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data.get("numero"), data.get("nom"), data.get("capacite"),
         data.get("type_salle", "amphitheatre"), data.get("equipements"),
         data.get("batiment"), data.get("etage"))
    )
    db.commit()
    return jsonify({"message": "Salle créée avec succès"}), 201

@salle_bp.route("/disponible")
def get_salles_disponibles():
    db = get_db()
    # Salles non utilisées dans les cours
    salles = db.execute("""
        SELECT s.* FROM salle s
        LEFT JOIN cours c ON s.id = c.salle_id
        WHERE c.id IS NULL OR c.jour_semaine != ?
    """, (request.args.get("jour"),)).fetchall()
    return jsonify([dict(s) for s in salles])

