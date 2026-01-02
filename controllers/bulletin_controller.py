from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
from functools import wraps

bulletin_bp = Blueprint("bulletin_bp", __name__, url_prefix="/bulletin")

def require_etudiant(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_type") != "etudiant":
            return redirect(url_for("auth_bp.login_page"))
        return f(*args, **kwargs)
    return decorated_function

@bulletin_bp.route("/etudiant/<int:etudiant_id>")
def get_bulletins_etudiant(etudiant_id):
    db = get_db()
    bulletins = db.execute("""
        SELECT bulletin.*, classe.nom as classe_nom, filiere.nom as filiere_nom
        FROM bulletin
        LEFT JOIN classe ON bulletin.classe_id = classe.id
        LEFT JOIN filiere ON bulletin.filiere_id = filiere.id
        WHERE bulletin.id_etudiant = ?
        ORDER BY bulletin.date_creation DESC
    """, (etudiant_id,)).fetchall()
    return jsonify([dict(b) for b in bulletins])

@bulletin_bp.route("/generate/<int:etudiant_id>")
def generate_bulletin(etudiant_id):
    db = get_db()
    
    # Récupérer l'étudiant
    etudiant = db.execute("SELECT * FROM etudiant WHERE id = ?", (etudiant_id,)).fetchone()
    if not etudiant:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    
    # Calculer la moyenne générale
    notes = db.execute("""
        SELECT note.valeur, note.coefficient, matiere.coefficient as matiere_coef
        FROM note
        JOIN matiere ON note.id_matiere = matiere.id
        WHERE note.id_etudiant = ?
    """, (etudiant_id,)).fetchall()
    
    if notes:
        total_points = sum(n["valeur"] * n["coefficient"] * n["matiere_coef"] for n in notes)
        total_coef = sum(n["coefficient"] * n["matiere_coef"] for n in notes)
        moyenne = total_points / total_coef if total_coef > 0 else 0
    else:
        moyenne = 0
    
    # Créer le bulletin
    db.execute(
        """INSERT INTO bulletin (id_etudiant, classe_id, filiere_id, periode, annee_scolaire, moyenne_generale)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (etudiant_id, etudiant["classe_id"], etudiant["filiere_id"],
         request.args.get("periode", "Semestre 1"), 
         request.args.get("annee_scolaire", "2024-2025"), moyenne)
    )
    db.commit()
    
    return jsonify({"message": "Bulletin généré avec succès", "moyenne": moyenne}), 201

