"""
Script de migration pour mettre à jour la base de données
Ajoute les colonnes manquantes si elles n'existent pas
"""
from app import app
from database.db import get_db

def migrate_database():
    with app.app_context():
        db = get_db()
        
        try:
            # Vérifier et ajouter la colonne commentaire à la table note
            try:
                db.execute("ALTER TABLE note ADD COLUMN commentaire TEXT")
                print("✅ Colonne 'commentaire' ajoutée à la table 'note'")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print("ℹ️  Colonne 'commentaire' existe déjà dans 'note'")
                else:
                    print(f"⚠️  Erreur lors de l'ajout de 'commentaire': {e}")
            
            # Vérifier et ajouter la colonne id_professeur à la table note
            try:
                db.execute("ALTER TABLE note ADD COLUMN id_professeur INTEGER")
                print("✅ Colonne 'id_professeur' ajoutée à la table 'note'")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print("ℹ️  Colonne 'id_professeur' existe déjà dans 'note'")
                else:
                    print(f"⚠️  Erreur lors de l'ajout de 'id_professeur' à 'note': {e}")
            
            # Vérifier et ajouter la colonne id_professeur à la table absence
            try:
                db.execute("ALTER TABLE absence ADD COLUMN id_professeur INTEGER")
                print("✅ Colonne 'id_professeur' ajoutée à la table 'absence'")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print("ℹ️  Colonne 'id_professeur' existe déjà dans 'absence'")
                else:
                    print(f"⚠️  Erreur lors de l'ajout de 'id_professeur' à 'absence': {e}")
            
            db.commit()
            print("\n✅ Migration terminée avec succès!")
            
        except Exception as e:
            db.rollback()
            print(f"❌ Erreur lors de la migration: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    migrate_database()

