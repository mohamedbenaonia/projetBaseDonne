from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from database.db import get_db
import hashlib

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user_type = data.get("user_type")
    email = data.get("email")
    password = data.get("password")
    
    if not all([user_type, email, password]):
        return jsonify({"error": "Tous les champs sont requis"}), 400
    
    db = get_db()
    hashed_password = hash_password(password)
    
    if user_type == "etudiant":
        auth = db.execute(
            "SELECT etudiant_id FROM etudiant_auth WHERE email = ? AND password = ?",
            (email, hashed_password)
        ).fetchone()
        if auth:
            etudiant = db.execute("SELECT * FROM etudiant WHERE id = ?", (auth["etudiant_id"],)).fetchone()
            if etudiant:
                session["user_type"] = "etudiant"
                session["user_id"] = etudiant["id"]
                session["user_name"] = f"{etudiant['nom']} {etudiant['prenom']}"
                return jsonify({"success": True, "redirect": "/etudiant/dashboard"})
    
    elif user_type == "professeur":
        auth = db.execute(
            "SELECT professeur_id FROM professeur_auth WHERE email = ? AND password = ?",
            (email, hashed_password)
        ).fetchone()
        if auth:
            prof = db.execute("SELECT * FROM professeur WHERE id = ?", (auth["professeur_id"],)).fetchone()
            if prof:
                session["user_type"] = "professeur"
                session["user_id"] = prof["id"]
                session["user_name"] = f"{prof['nom']} {prof['prenom']}"
                return jsonify({"success": True, "redirect": "/professeur/dashboard"})
    
    elif user_type == "administrateur":
        # Pour les admins, on peut accepter le mot de passe en clair ou hashé
        admin = db.execute(
            "SELECT * FROM administrateur WHERE username = ?",
            (email,)
        ).fetchone()
        if admin and (admin["password"] == hashed_password or admin["password"] == password):
            session["user_type"] = "administrateur"
            session["user_id"] = admin["id"]
            session["user_name"] = admin["username"]
            return jsonify({"success": True, "redirect": "/administrateur/dashboard"})
    
    return jsonify({"error": "Email ou mot de passe incorrect"}), 401

@auth_bp.route("/register", methods=["GET"])
def register_page():
    db = get_db()
    try:
        filieres = db.execute("SELECT * FROM filiere ORDER BY nom").fetchall()
        filieres_list = [dict(f) for f in filieres]
    except Exception as e:
        # Si la table n'existe pas encore, retourner une liste vide
        print(f"Erreur lors de la récupération des filières: {e}")
        filieres_list = []
    
    return render_template("register.html", filieres=filieres_list)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user_type = data.get("user_type")
    
    if not user_type:
        return jsonify({"error": "Type d'utilisateur requis"}), 400
    
    if not data.get("password"):
        return jsonify({"error": "Mot de passe requis"}), 400
    
    db = get_db()
    hashed_password = hash_password(data.get("password", ""))
    
    try:
        if user_type == "etudiant":
            # Vérifier si l'email existe déjà
            existing = db.execute("SELECT id FROM etudiant_auth WHERE email = ?", 
                                 (data.get("email"),)).fetchone()
            if existing:
                return jsonify({"error": "Cet email est déjà utilisé"}), 400
            
            # Créer l'étudiant
            filiere_id = data.get("filiere_id")
            if not filiere_id:
                return jsonify({"error": "Filière requise"}), 400
            
            try:
                filiere_id = int(filiere_id)
            except (ValueError, TypeError):
                return jsonify({"error": "Filière invalide"}), 400
            
            # Vérifier que la filière existe
            filiere_check = db.execute("SELECT id FROM filiere WHERE id = ?", (filiere_id,)).fetchone()
            if not filiere_check:
                return jsonify({"error": "Filière introuvable"}), 400
            
            db.execute(
                "INSERT INTO etudiant (nom, prenom, email, filiere_id) VALUES (?, ?, ?, ?)",
                (data.get("nom"), data.get("prenom"), data.get("email"), filiere_id)
            )
            etudiant = db.execute("SELECT id FROM etudiant WHERE email = ?", 
                                 (data.get("email"),)).fetchone()
            
            if etudiant:
                # Créer les identifiants
                db.execute(
                    "INSERT INTO etudiant_auth (etudiant_id, email, password) VALUES (?, ?, ?)",
                    (etudiant["id"], data.get("email"), hashed_password)
                )
                db.commit()
                return jsonify({"success": True, "message": "Compte étudiant créé avec succès", "redirect": "/auth/login"})
            else:
                return jsonify({"error": "Erreur lors de la création de l'étudiant"}), 500
        
        elif user_type == "professeur":
            # Vérifier si l'email existe déjà
            existing = db.execute("SELECT id FROM professeur_auth WHERE email = ?", 
                                 (data.get("email"),)).fetchone()
            if existing:
                return jsonify({"error": "Cet email est déjà utilisé"}), 400
            
            # Créer le professeur
            filiere_id = data.get("filiere_id")
            if not filiere_id:
                return jsonify({"error": "Filière requise"}), 400
            
            try:
                filiere_id = int(filiere_id)
            except (ValueError, TypeError):
                return jsonify({"error": "Filière invalide"}), 400
            
            # Vérifier que la filière existe
            filiere_check = db.execute("SELECT id FROM filiere WHERE id = ?", (filiere_id,)).fetchone()
            if not filiere_check:
                return jsonify({"error": "Filière introuvable"}), 400
            
            db.execute(
                "INSERT INTO professeur (nom, prenom, filiere_id) VALUES (?, ?, ?)",
                (data.get("nom"), data.get("prenom"), filiere_id)
            )
            prof = db.execute("SELECT id FROM professeur WHERE nom = ? AND prenom = ?", 
                             (data.get("nom"), data.get("prenom"))).fetchone()
            
            if prof:
                # Créer les identifiants
                db.execute(
                    "INSERT INTO professeur_auth (professeur_id, email, password) VALUES (?, ?, ?)",
                    (prof["id"], data.get("email"), hashed_password)
                )
                db.commit()
                return jsonify({"success": True, "message": "Compte professeur créé avec succès", "redirect": "/auth/login"})
            else:
                return jsonify({"error": "Erreur lors de la création du professeur"}), 500
        
        elif user_type == "administrateur":
            # Vérifier si le username existe déjà
            existing = db.execute("SELECT id FROM administrateur WHERE username = ?", 
                                 (data.get("username"),)).fetchone()
            if existing:
                return jsonify({"error": "Ce nom d'utilisateur est déjà utilisé"}), 400
            
            # Créer l'administrateur
            db.execute(
                "INSERT INTO administrateur (username, password) VALUES (?, ?)",
                (data.get("username"), hashed_password)
            )
            db.commit()
            return jsonify({"success": True, "message": "Compte administrateur créé avec succès", "redirect": "/auth/login"})
        
        return jsonify({"error": "Type d'utilisateur invalide"}), 400
    
    except Exception as e:
        import traceback
        db.rollback()
        error_details = str(e)
        print(f"Erreur lors de l'inscription: {error_details}")
        print(traceback.format_exc())
        return jsonify({"error": f"Erreur lors de la création du compte: {error_details}"}), 500

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_bp.login_page"))

def require_login(user_type=None):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth_bp.login_page"))
            if user_type and session.get("user_type") != user_type:
                return jsonify({"error": "Accès non autorisé"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

