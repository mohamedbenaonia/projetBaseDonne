from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

etudiant_bp = Blueprint("etudiant_bp", __name__, url_prefix="/etudiant")

def require_etudiant(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_type") != "etudiant":
            return redirect(url_for("auth_bp.login_page"))
        return f(*args, **kwargs)
    return decorated_function

@etudiant_bp.route("/dashboard")
@require_etudiant
def dashboard():
    db = get_db()
    id_etudiant = session["user_id"]
    etudiant = db.execute("SELECT * FROM etudiant WHERE id = ?", (id_etudiant,)).fetchone()
    
    if etudiant is None:
        return redirect(url_for("auth_bp.login_page"))
    
    # Récupérer toutes les matières disponibles
    cours = db.execute("SELECT * FROM cours").fetchall()
    
    return render_template("etudiant_dashboard.html",
                           etudiant=dict(etudiant),
                           cours=[dict(c) for c in cours])

@etudiant_bp.route("/api/notes/<int:id_cours>")
@require_etudiant
def get_notes_by_cours(id_cours):
    db = get_db()
    id_etudiant = session["user_id"]
    try:
        notes = db.execute(
            """SELECT note.id, cours.nom as cours_nom, note.valeur, 
               COALESCE(note.commentaire, '') as commentaire, 
               COALESCE(professeur.nom, '') as prof_nom, 
               COALESCE(professeur.prenom, '') as prof_prenom
               FROM note 
               LEFT JOIN cours ON note.id_cours = cours.id
               LEFT JOIN professeur ON note.id_professeur = professeur.id
               WHERE note.id_etudiant = ? AND note.id_cours = ?""",
            (id_etudiant, id_cours)
        ).fetchall()
        return jsonify([dict(n) for n in notes])
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des notes: {str(e)}"}), 500

@etudiant_bp.route("/api/absences/<int:id_cours>")
@require_etudiant
def get_absences_by_cours(id_cours):
    db = get_db()
    id_etudiant = session["user_id"]
    try:
        absences = db.execute(
            """SELECT absence.id, cours.nom as cours_nom, absence.date_absence,
               COALESCE(professeur.nom, '') as prof_nom, 
               COALESCE(professeur.prenom, '') as prof_prenom,
               (SELECT COUNT(*) FROM absence a2 WHERE a2.id_etudiant = absence.id_etudiant AND a2.id_cours = absence.id_cours) as total_absences
               FROM absence 
               LEFT JOIN cours ON absence.id_cours = cours.id
               LEFT JOIN professeur ON absence.id_professeur = professeur.id
               WHERE absence.id_etudiant = ? AND absence.id_cours = ?
               ORDER BY absence.date_absence DESC""",
            (id_etudiant, id_cours)
        ).fetchall()
        return jsonify([dict(a) for a in absences])
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération des absences: {str(e)}"}), 500

# GET JSON
@etudiant_bp.route("/", methods=["GET"])
def get_etudiants():
    db = get_db()
    rows = db.execute("SELECT * FROM etudiant").fetchall()
    return jsonify([dict(r) for r in rows])

# POST JSON
@etudiant_bp.route("/", methods=["POST"])
def add_etudiant():
    data = request.json
    db = get_db()
    db.execute(
        "INSERT INTO etudiant (nom, prenom, email) VALUES (?, ?, ?)",
        (data["nom"], data["prenom"], data["email"])
    )
    db.commit()
    return jsonify({"message": "Étudiant ajouté"}), 201

# Page HTML
@etudiant_bp.route("/page")
def etudiant_page():
    return render_template("etudiant.html")
