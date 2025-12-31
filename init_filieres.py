"""
Script pour initialiser la base de données et créer les filières
"""
import sys
from app import app
from database.db import get_db

def init_filieres():
    with app.app_context():
        db = get_db()
        
        print("=" * 60)
        print("INITIALISATION DE LA BASE DE DONNÉES")
        print("=" * 60)
        
        # 1. Créer toutes les tables
        print("\n📦 Création des tables...")
        try:
            with open("schema.sql", "r", encoding="utf-8") as f:
                schema = f.read()
            db.executescript(schema)
            db.commit()
            print("✅ Tables créées")
        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg.lower() or "duplicate" in error_msg.lower():
                print("ℹ️  Les tables existent déjà")
            else:
                print(f"⚠️  Erreur lors de la création des tables: {e}")
        
        # 2. Exécuter la migration pour ajouter les colonnes manquantes
        print("\n🔄 Exécution de la migration...")
        try:
            from migrate_to_15_tables import migrate_to_15_tables
            migrate_to_15_tables()
        except Exception as e:
            print(f"⚠️  Erreur lors de la migration: {e}")
        
        # 3. Vérifier si la table filiere existe
        print("\n🔍 Vérification de la table 'filiere'...")
        try:
            test = db.execute("SELECT COUNT(*) as count FROM filiere").fetchone()
            print("✅ Table 'filiere' existe")
        except Exception as e:
            print(f"❌ Table 'filiere' n'existe pas: {e}")
            print("   Création de la table...")
            db.execute("""
                CREATE TABLE IF NOT EXISTS filiere (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT UNIQUE NOT NULL,
                    description TEXT,
                    responsable_id INTEGER,
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()
            print("✅ Table 'filiere' créée")
        
        # 4. Créer les filières de base
        print("\n📚 Création des filières...")
        filieres_test = [
            ("Informatique", "Filière d'informatique et développement logiciel"),
            ("Mathématiques", "Filière de mathématiques appliquées et pures"),
            ("Physique", "Filière de physique fondamentale et appliquée"),
            ("Chimie", "Filière de chimie organique et inorganique"),
            ("Biologie", "Filière de biologie et sciences de la vie"),
            ("Économie", "Filière d'économie et gestion"),
            ("Droit", "Filière de droit et sciences juridiques"),
            ("Lettres", "Filière de lettres et langues")
        ]
        
        created_count = 0
        for nom, desc in filieres_test:
            try:
                db.execute(
                    "INSERT OR IGNORE INTO filiere (nom, description) VALUES (?, ?)",
                    (nom, desc)
                )
                created_count += 1
                print(f"   ✅ Filière '{nom}' créée")
            except Exception as e:
                error_msg = str(e)
                if "UNIQUE constraint" in error_msg or "already exists" in error_msg.lower():
                    print(f"   ℹ️  Filière '{nom}' existe déjà")
                else:
                    print(f"   ⚠️  Erreur pour '{nom}': {e}")
        
        db.commit()
        
        # 5. Vérifier
        try:
            filieres = db.execute("SELECT * FROM filiere ORDER BY nom").fetchall()
            print(f"\n✅ {len(filieres)} filières disponibles:")
            for f in filieres:
                print(f"   - ID {f['id']}: {f['nom']}")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
        
        print("\n" + "=" * 60)
        print("✅ INITIALISATION TERMINÉE!")
        print("=" * 60)
        print(f"\n💡 {created_count} nouvelles filières créées.")
        print("💡 Vous pouvez maintenant créer des comptes avec ces filières.")

if __name__ == "__main__":
    try:
        init_filieres()
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

