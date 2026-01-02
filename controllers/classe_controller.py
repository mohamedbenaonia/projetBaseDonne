from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

classe_bp = Blueprint("classe_bp", __name__, url_prefix="/classe")

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_type") != "administrateur":
            return redirect(url_for("auth_bp.login_page"))
        return f(*args, **kwargs)
    return decorated_function

@classe_bp.route("/", methods=["GET"])
def get_classes():
    db = get_db()
    classes = db.execute("""
        SELECT classe.*, filiere.nom as filiere_nom, 
               professeur.nom as prof_nom, professeur.prenom as prof_prenom
        FROM classe
        LEFT JOIN filiere ON classe.filiere_id = filiere.id
        LEFT JOIN professeur ON classe.professeur_principal_id = professeur.id
    """).fetchall()
    return jsonify([dict(c) for c in classes])

@classe_bp.route("/", methods=["POST"])
@require_admin
def add_classe():
    data = request.json
    db = get_db()
    db.execute(
        """INSERT INTO classe (nom, niveau, filiere_id, professeur_principal_id, capacite_max, annee_scolaire)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (data.get("nom"), data.get("niveau"), data.get("filiere_id"), 
         data.get("professeur_principal_id"), data.get("capacite_max", 30), 
         data.get("annee_scolaire"))
    )
    db.commit()
    return jsonify({"message": "Classe créée avec succès"}), 201

@classe_bp.route("/<int:classe_id>/etudiants")
def get_etudiants_classe(classe_id):
    db = get_db()
    etudiants = db.execute(
        "SELECT * FROM etudiant WHERE classe_id = ?", (classe_id,)
    ).fetchall()
    return jsonify([dict(e) for e in etudiants])

