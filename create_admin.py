"""
Script pour créer un compte administrateur rapidement
"""
from app import app
from database.db import get_db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_admin(username="admin", password="admin123"):
    with app.app_context():
        db = get_db()
        
        # Vérifier si l'admin existe déjà
        existing = db.execute("SELECT id FROM administrateur WHERE username = ?", (username,)).fetchone()
        if existing:
            print(f"⚠️  L'administrateur '{username}' existe déjà")
            return False
        
        # Créer l'administrateur
        hashed_password = hash_password(password)
        db.execute(
            "INSERT INTO administrateur (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        db.commit()
        
        print("=" * 60)
        print("✅ ADMINISTRATEUR CRÉÉ AVEC SUCCÈS!")
        print("=" * 60)
        print(f"👤 Username: {username}")
        print(f"🔑 Password: {password}")
        print("\n💡 Vous pouvez maintenant vous connecter avec ces identifiants.")
        return True

if __name__ == "__main__":
    import sys
    username = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin123"
    create_admin(username, password)

