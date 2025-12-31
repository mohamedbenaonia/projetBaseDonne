from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

examen_bp = Blueprint("examen_bp", __name__, url_prefix="/examen")

def require_professeur(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_type") != "professeur":
            return redirect(url_for("auth_bp.login_page"))
        return f(*args, **kwargs)
    return decorated_function

@examen_bp.route("/", methods=["GET"])
def get_examens():
    db = get_db()
    classe_id = request.args.get("classe_id")
    if classe_id:
        examens = db.execute("""
            SELECT examen.*, matiere.nom as matiere_nom, classe.nom as classe_nom, salle.numero as salle_numero
            FROM examen
            JOIN matiere ON examen.matiere_id = matiere.id
            LEFT JOIN classe ON examen.classe_id = classe.id
            LEFT JOIN salle ON examen.salle_id = salle.id
            WHERE examen.classe_id = ?
            ORDER BY examen.date_examen
        """, (classe_id,)).fetchall()
    else:
        examens = db.execute("""
            SELECT examen.*, matiere.nom as matiere_nom, classe.nom as classe_nom, salle.numero as salle_numero
            FROM examen
            JOIN matiere ON examen.matiere_id = matiere.id
            LEFT JOIN classe ON examen.classe_id = classe.id
            LEFT JOIN salle ON examen.salle_id = salle.id
            ORDER BY examen.date_examen
        """).fetchall()
    return jsonify([dict(e) for e in examens])

@examen_bp.route("/", methods=["POST"])
@require_professeur
def add_examen():
    data = request.json
    db = get_db()
    db.execute(
        """INSERT INTO examen (nom, matiere_id, classe_id, date_examen, heure_debut, heure_fin, 
           salle_id, type_examen, coefficient, duree_minutes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (data.get("nom"), data.get("matiere_id"), data.get("classe_id"),
         data.get("date_examen"), data.get("heure_debut"), data.get("heure_fin"),
         data.get("salle_id"), data.get("type_examen", "controle"),
         data.get("coefficient", 1.0), data.get("duree_minutes"))
    )
    db.commit()
    return jsonify({"message": "Examen créé avec succès"}), 201

