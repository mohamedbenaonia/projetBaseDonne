"""
Script de démarrage avec vérifications
"""
import sys
import os

print("=" * 60)
print("🚀 DÉMARRAGE DE LA PLATEFORME UNIVERSITAIRE")
print("=" * 60)

# Vérifier que la base de données existe
if not os.path.exists("database/database.db"):
    print("\n⚠️  Base de données non trouvée. Création en cours...")
    from app import app
    with app.app_context():
        from database.db import init_db
        init_db()
    print("✅ Base de données créée")

# Vérifier les imports
print("\n📦 Vérification des dépendances...")
try:
    from flask import Flask
    print("✅ Flask installé")
except ImportError:
    print("❌ Flask non installé. Exécutez: pip install flask")
    sys.exit(1)

# Vérifier la structure de la base de données
print("\n🔍 Vérification de la structure de la base de données...")
try:
    from app import app
    from database.db import get_db
    
    with app.app_context():
        db = get_db()
        
        # Vérifier les tables essentielles
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [t[0] for t in tables]
        
        required_tables = ['administrateur', 'filiere', 'professeur', 'etudiant', 'cours', 
                          'note', 'absence', 'professeur_auth', 'etudiant_auth']
        
        missing_tables = [t for t in required_tables if t not in table_names]
        
        if missing_tables:
            print(f"⚠️  Tables manquantes: {', '.join(missing_tables)}")
            print("   Exécution de la migration...")
            from migrate_to_15_tables import migrate_to_15_tables
            migrate_to_15_tables()
        else:
            print(f"✅ {len(table_names)} tables trouvées")
        
        # Vérifier les colonnes critiques
        note_cols = [c[1] for c in db.execute("PRAGMA table_info(note)").fetchall()]
        absence_cols = [c[1] for c in db.execute("PRAGMA table_info(absence)").fetchall()]
        
        if 'commentaire' not in note_cols or 'id_professeur' not in note_cols:
            print("⚠️  Colonnes manquantes dans 'note'. Exécution de la migration...")
            from migrate_to_15_tables import migrate_to_15_tables
            migrate_to_15_tables()
        elif 'id_professeur' not in absence_cols:
            print("⚠️  Colonnes manquantes dans 'absence'. Exécution de la migration...")
            from migrate_to_15_tables import migrate_to_15_tables
            migrate_to_15_tables()
        else:
            print("✅ Structure de la base de données OK")
            
except Exception as e:
    print(f"❌ Erreur lors de la vérification: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Démarrer l'application
print("\n" + "=" * 60)
print("✅ TOUTES LES VÉRIFICATIONS SONT OK")
print("=" * 60)
print("\n🌐 Démarrage du serveur Flask...")
print("📍 Accédez à: http://localhost:5000")
print("\n⚠️  Appuyez sur Ctrl+C pour arrêter le serveur\n")

from app import app

if __name__ == "__main__":
    with app.app_context():
        from database.db import get_db
        with open("schema.sql", encoding="utf-8") as f:
            get_db().executescript(f.read())
    app.run(debug=True, host='0.0.0.0', port=5000)

