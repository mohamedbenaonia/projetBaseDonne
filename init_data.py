"""
Script d'initialisation des données de test
Exécutez ce script une fois pour créer des utilisateurs de test
"""
from database.db import get_db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_test_data():
    db = get_db()
    
    # Créer une filière
    db.execute("INSERT OR IGNORE INTO filiere (nom) VALUES (?)", ("Informatique",))
    db.execute("INSERT OR IGNORE INTO filiere (nom) VALUES (?)", ("Mathématiques",))
    filiere_info = db.execute("SELECT id FROM filiere WHERE nom = ?", ("Informatique",)).fetchone()
    filiere_id = filiere_info["id"] if filiere_info else 1
    
    # Créer un administrateur
    admin_password = hash_password("admin123")
    db.execute("INSERT OR IGNORE INTO administrateur (username, password) VALUES (?, ?)",
               ("admin", admin_password))
    
    # Créer un professeur
    db.execute("INSERT OR IGNORE INTO professeur (nom, prenom, filiere_id) VALUES (?, ?, ?)",
               ("Dupont", "Jean", filiere_id))
    prof = db.execute("SELECT id FROM professeur WHERE nom = ? AND prenom = ?", 
                     ("Dupont", "Jean")).fetchone()
    if prof:
        prof_id = prof["id"]
        prof_password = hash_password("prof123")
        db.execute("INSERT OR IGNORE INTO professeur_auth (professeur_id, email, password) VALUES (?, ?, ?)",
                   (prof_id, "prof@example.com", prof_password))
    
    # Créer un étudiant
    db.execute("INSERT OR IGNORE INTO etudiant (nom, prenom, email, filiere_id) VALUES (?, ?, ?, ?)",
               ("Martin", "Sophie", "sophie@example.com", filiere_id))
    etudiant = db.execute("SELECT id FROM etudiant WHERE email = ?", 
                         ("sophie@example.com",)).fetchone()
    if etudiant:
        etudiant_id = etudiant["id"]
        etudiant_password = hash_password("etudiant123")
        db.execute("INSERT OR IGNORE INTO etudiant_auth (etudiant_id, email, password) VALUES (?, ?, ?)",
                   (etudiant_id, "sophie@example.com", etudiant_password))
    
    # Créer des cours
    db.execute("INSERT OR IGNORE INTO cours (nom, filiere_id) VALUES (?, ?)",
               ("Programmation Python", filiere_id))
    db.execute("INSERT OR IGNORE INTO cours (nom, filiere_id) VALUES (?, ?)",
               ("Base de données", filiere_id))
    db.execute("INSERT OR IGNORE INTO cours (nom, filiere_id) VALUES (?, ?)",
               ("Algorithmes", filiere_id))
    
    db.commit()
    print("✅ Données de test initialisées avec succès !")
    print("\nComptes de test créés :")
    print("👤 Administrateur:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n👨‍🏫 Professeur:")
    print("   Email: prof@example.com")
    print("   Password: prof123")
    print("\n👨‍🎓 Étudiant:")
    print("   Email: sophie@example.com")
    print("   Password: etudiant123")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        init_test_data()

