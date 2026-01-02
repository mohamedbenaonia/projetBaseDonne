from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

administrateur_bp = Blueprint("administrateur_bp", __name__, url_prefix="/administrateur")

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_type") != "administrateur":
            return redirect(url_for("auth_bp.login_page"))
        return f(*args, **kwargs)
    return decorated_function

@administrateur_bp.route("/dashboard")
@require_admin
def dashboard():
    db = get_db()
    
    # Statistiques globales
    total_etudiants = db.execute("SELECT COUNT(*) as count FROM etudiant").fetchone()["count"]
    total_professeurs = db.execute("SELECT COUNT(*) as count FROM professeur").fetchone()["count"]
    total_cours = db.execute("SELECT COUNT(*) as count FROM cours").fetchone()["count"]
    total_notes = db.execute("SELECT COUNT(*) as count FROM note").fetchone()["count"]
    total_absences = db.execute("SELECT COUNT(*) as count FROM absence").fetchone()["count"]
    
    # Récupérer toutes les données
    etudiants = db.execute("SELECT * FROM etudiant").fetchall()
    professeurs = db.execute("SELECT * FROM professeur").fetchall()
    cours = db.execute("SELECT * FROM cours").fetchall()
    filieres = db.execute("SELECT * FROM filiere").fetchall()
    
    # Notes récentes
    notes_recentes = db.execute(
        """SELECT note.id, etudiant.nom as etudiant_nom, etudiant.prenom as etudiant_prenom,
           cours.nom as cours_nom, note.valeur, note.commentaire,
           professeur.nom as prof_nom, professeur.prenom as prof_prenom
           FROM note
           JOIN etudiant ON note.id_etudiant = etudiant.id
           JOIN cours ON note.id_cours = cours.id
           JOIN professeur ON note.id_professeur = professeur.id
           ORDER BY note.id DESC LIMIT 10"""
    ).fetchall()
    
    # Absences récentes
    absences_recentes = db.execute(
        """SELECT absence.id, etudiant.nom as etudiant_nom, etudiant.prenom as etudiant_prenom,
           cours.nom as cours_nom, absence.date_absence,
           professeur.nom as prof_nom, professeur.prenom as prof_prenom
           FROM absence
           JOIN etudiant ON absence.id_etudiant = etudiant.id
           JOIN cours ON absence.id_cours = cours.id
           JOIN professeur ON absence.id_professeur = professeur.id
           ORDER BY absence.date_absence DESC LIMIT 10"""
    ).fetchall()
    
    return render_template("administrateur_dashboard.html",
                           total_etudiants=total_etudiants,
                           total_professeurs=total_professeurs,
                           total_cours=total_cours,
                           total_notes=total_notes,
                           total_absences=total_absences,
                           etudiants=[dict(e) for e in etudiants],
                           professeurs=[dict(p) for p in professeurs],
                           cours=[dict(c) for c in cours],
                           filieres=[dict(f) for f in filieres],
                           notes_recentes=[dict(n) for n in notes_recentes],
                           absences_recentes=[dict(a) for a in absences_recentes])

# GET all
@administrateur_bp.route("/", methods=["GET"])
def get_admins():
    db = get_db()
    rows = db.execute("SELECT * FROM administrateur").fetchall()
    return jsonify([dict(r) for r in rows])

# POST
@administrateur_bp.route("/", methods=["POST"])
def add_admin():
    data = request.json
    db = get_db()
    db.execute(
        "INSERT INTO administrateur (username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )
    db.commit()
    return jsonify({"message": "Administrateur ajouté"}), 201

# PAGE HTML
@administrateur_bp.route("/page")
def admin_page():
    return render_template("administrateur.html")
