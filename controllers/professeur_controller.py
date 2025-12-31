from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

professeur_bp = Blueprint("professeur_bp", __name__, url_prefix="/professeur")

def require_professeur(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_type") != "professeur":
            return redirect(url_for("auth_bp.login_page"))
        return f(*args, **kwargs)
    return decorated_function

@professeur_bp.route("/dashboard")
@require_professeur
def dashboard():
    
    db = get_db()
    id_prof = session["user_id"]
    prof = db.execute("SELECT * FROM professeur WHERE id = ?", (id_prof,)).fetchone()
    
    if prof is None:
        return redirect(url_for("auth_bp.login_page"))
    
    filiere_id = prof["filiere_id"]
    
    # Récupérer le nom de la filière
    filiere_info = None
    if filiere_id:
        filiere_info = db.execute("SELECT * FROM filiere WHERE id = ?", (filiere_id,)).fetchone()
    
    # Récupérer les étudiants de la même filière
    if filiere_id:
        etudiants = db.execute(
            "SELECT etudiant.*, filiere.nom as filiere_nom FROM etudiant LEFT JOIN filiere ON etudiant.filiere_id = filiere.id WHERE etudiant.filiere_id = ?", 
            (filiere_id,)
        ).fetchall()
    else:
        etudiants = []
    
    # Récupérer tous les étudiants pour information (pour debug/aide)
    tous_etudiants = db.execute(
        "SELECT etudiant.*, filiere.nom as filiere_nom FROM etudiant LEFT JOIN filiere ON etudiant.filiere_id = filiere.id"
    ).fetchall()
    
    # Récupérer les cours de la filière
    if filiere_id:
        cours = db.execute("SELECT * FROM cours WHERE filiere_id = ?", (filiere_id,)).fetchall()
    else:
        # Si pas de filière, récupérer tous les cours
        cours = db.execute("SELECT * FROM cours").fetchall()
    
    # Statistiques
    total_etudiants = len(etudiants)
    total_cours = len(cours)
    total_etudiants_tous = len(tous_etudiants)
    
    return render_template("professeur_dashboard.html",
                           prof=dict(prof),
                           filiere=dict(filiere_info) if filiere_info else None,
                           etudiants=[dict(e) for e in etudiants],
                           cours=[dict(c) for c in cours],
                           tous_etudiants=[dict(e) for e in tous_etudiants],
                           total_etudiants=total_etudiants,
                           total_etudiants_tous=total_etudiants_tous,
                           total_cours=total_cours)

@professeur_bp.route("/api/etudiant/<int:id_etudiant>/notes")
@require_professeur
def get_etudiant_notes(id_etudiant):
    db = get_db()
    id_prof = session["user_id"]
    notes = db.execute(
        """SELECT note.id, cours.nom as cours_nom, note.valeur, note.commentaire, note.id_cours
           FROM note 
           JOIN cours ON note.id_cours = cours.id 
           WHERE note.id_etudiant = ? AND note.id_professeur = ?""",
        (id_etudiant, id_prof)
    ).fetchall()
    return jsonify([dict(n) for n in notes])

@professeur_bp.route("/api/etudiant/<int:id_etudiant>/absences")
@require_professeur
def get_etudiant_absences(id_etudiant):
    db = get_db()
    id_prof = session["user_id"]
    absences = db.execute(
        """SELECT absence.id, cours.nom as cours_nom, absence.date_absence, absence.id_cours,
           (SELECT COUNT(*) FROM absence a2 WHERE a2.id_etudiant = absence.id_etudiant AND a2.id_cours = absence.id_cours) as total_absences
           FROM absence 
           JOIN cours ON absence.id_cours = cours.id 
           WHERE absence.id_etudiant = ? AND absence.id_professeur = ?
           ORDER BY absence.date_absence DESC""",
        (id_etudiant, id_prof)
    ).fetchall()
    return jsonify([dict(a) for a in absences])

# Routes API pour compatibilité
@professeur_bp.route("/notes/page/<int:id_prof>")
def notes_page(id_prof):
    return redirect(url_for("professeur_bp.dashboard"))

@professeur_bp.route("/absences/page/<int:id_prof>")
def absences_page(id_prof):
    return redirect(url_for("professeur_bp.dashboard"))
