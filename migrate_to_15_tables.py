"""
Script de migration pour passer de 9 à 15 tables
Ajoute les nouvelles tables et colonnes manquantes
"""
from app import app
from database.db import get_db

def migrate_to_15_tables():
    with app.app_context():
        db = get_db()
        
        print("=" * 60)
        print("MIGRATION VERS 15 TABLES")
        print("=" * 60)
        
        try:
            # 1. Ajouter les colonnes manquantes aux tables existantes
            print("\n📝 Ajout des colonnes manquantes aux tables existantes...")
            
            # Table etudiant
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN telephone TEXT")
                print("✅ Colonne 'telephone' ajoutée à 'etudiant'")
            except: pass
            
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN date_naissance TEXT")
                print("✅ Colonne 'date_naissance' ajoutée à 'etudiant'")
            except: pass
            
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN adresse TEXT")
                print("✅ Colonne 'adresse' ajoutée à 'etudiant'")
            except: pass
            
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN classe_id INTEGER")
                print("✅ Colonne 'classe_id' ajoutée à 'etudiant'")
            except: pass
            
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN numero_etudiant TEXT")
                print("✅ Colonne 'numero_etudiant' ajoutée à 'etudiant'")
            except: pass
            
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN date_inscription TEXT")
                print("✅ Colonne 'date_inscription' ajoutée à 'etudiant'")
            except: pass
            
            try:
                db.execute("ALTER TABLE etudiant ADD COLUMN statut TEXT DEFAULT 'actif'")
                print("✅ Colonne 'statut' ajoutée à 'etudiant'")
            except: pass
            
            # Table professeur
            try:
                db.execute("ALTER TABLE professeur ADD COLUMN email TEXT")
                print("✅ Colonne 'email' ajoutée à 'professeur'")
            except: pass
            
            try:
                db.execute("ALTER TABLE professeur ADD COLUMN telephone TEXT")
                print("✅ Colonne 'telephone' ajoutée à 'professeur'")
            except: pass
            
            try:
                db.execute("ALTER TABLE professeur ADD COLUMN departement_id INTEGER")
                print("✅ Colonne 'departement_id' ajoutée à 'professeur'")
            except: pass
            
            try:
                db.execute("ALTER TABLE professeur ADD COLUMN specialite TEXT")
                print("✅ Colonne 'specialite' ajoutée à 'professeur'")
            except: pass
            
            try:
                db.execute("ALTER TABLE professeur ADD COLUMN date_embauche TEXT")
                print("✅ Colonne 'date_embauche' ajoutée à 'professeur'")
            except: pass
            
            try:
                db.execute("ALTER TABLE professeur ADD COLUMN statut TEXT DEFAULT 'actif'")
                print("✅ Colonne 'statut' ajoutée à 'professeur'")
            except: pass
            
            # Table filiere
            try:
                db.execute("ALTER TABLE filiere ADD COLUMN description TEXT")
                print("✅ Colonne 'description' ajoutée à 'filiere'")
            except: pass
            
            try:
                db.execute("ALTER TABLE filiere ADD COLUMN responsable_id INTEGER")
                print("✅ Colonne 'responsable_id' ajoutée à 'filiere'")
            except: pass
            
            try:
                db.execute("ALTER TABLE filiere ADD COLUMN date_creation TEXT")
                print("✅ Colonne 'date_creation' ajoutée à 'filiere'")
            except: pass
            
            # Table cours
            try:
                db.execute("ALTER TABLE cours ADD COLUMN matiere_id INTEGER")
                print("✅ Colonne 'matiere_id' ajoutée à 'cours'")
            except: pass
            
            try:
                db.execute("ALTER TABLE cours ADD COLUMN classe_id INTEGER")
                print("✅ Colonne 'classe_id' ajoutée à 'cours'")
            except: pass
            
            try:
                db.execute("ALTER TABLE cours ADD COLUMN salle_id INTEGER")
                print("✅ Colonne 'salle_id' ajoutée à 'cours'")
            except: pass
            
            try:
                db.execute("ALTER TABLE cours ADD COLUMN jour_semaine TEXT")
                print("✅ Colonne 'jour_semaine' ajoutée à 'cours'")
            except: pass
            
            try:
                db.execute("ALTER TABLE cours ADD COLUMN heure_debut TEXT")
                print("✅ Colonne 'heure_debut' ajoutée à 'cours'")
            except: pass
            
            try:
                db.execute("ALTER TABLE cours ADD COLUMN heure_fin TEXT")
                print("✅ Colonne 'heure_fin' ajoutée à 'cours'")
            except: pass
            
            # Table note
            try:
                db.execute("ALTER TABLE note ADD COLUMN id_matiere INTEGER")
                print("✅ Colonne 'id_matiere' ajoutée à 'note'")
            except: pass
            
            try:
                db.execute("ALTER TABLE note ADD COLUMN type_note TEXT DEFAULT 'controle'")
                print("✅ Colonne 'type_note' ajoutée à 'note'")
            except: pass
            
            try:
                db.execute("ALTER TABLE note ADD COLUMN coefficient REAL DEFAULT 1.0")
                print("✅ Colonne 'coefficient' ajoutée à 'note'")
            except: pass
            
            try:
                db.execute("ALTER TABLE note ADD COLUMN date_note TEXT")
                print("✅ Colonne 'date_note' ajoutée à 'note'")
            except: pass
            
            # Table absence
            try:
                db.execute("ALTER TABLE absence ADD COLUMN heure_debut TEXT")
                print("✅ Colonne 'heure_debut' ajoutée à 'absence'")
            except: pass
            
            try:
                db.execute("ALTER TABLE absence ADD COLUMN heure_fin TEXT")
                print("✅ Colonne 'heure_fin' ajoutée à 'absence'")
            except: pass
            
            try:
                db.execute("ALTER TABLE absence ADD COLUMN justifiee INTEGER DEFAULT 0")
                print("✅ Colonne 'justifiee' ajoutée à 'absence'")
            except: pass
            
            try:
                db.execute("ALTER TABLE absence ADD COLUMN motif TEXT")
                print("✅ Colonne 'motif' ajoutée à 'absence'")
            except: pass
            
            try:
                db.execute("ALTER TABLE absence ADD COLUMN date_justification TEXT")
                print("✅ Colonne 'date_justification' ajoutée à 'absence'")
            except: pass
            
            # Table administrateur
            try:
                db.execute("ALTER TABLE administrateur ADD COLUMN date_creation TEXT")
                print("✅ Colonne 'date_creation' ajoutée à 'administrateur'")
            except: pass
            
            db.commit()
            
            # 2. Créer les nouvelles tables
            print("\n📦 Création des nouvelles tables...")
            
            # Table departement
            db.execute("""
                CREATE TABLE IF NOT EXISTS departement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT UNIQUE NOT NULL,
                    description TEXT,
                    chef_departement_id INTEGER,
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table 'departement' créée")
            
            # Table classe
            db.execute("""
                CREATE TABLE IF NOT EXISTS classe (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    niveau TEXT,
                    filiere_id INTEGER NOT NULL,
                    professeur_principal_id INTEGER,
                    capacite_max INTEGER DEFAULT 30,
                    annee_scolaire TEXT,
                    FOREIGN KEY(filiere_id) REFERENCES filiere(id),
                    FOREIGN KEY(professeur_principal_id) REFERENCES professeur(id)
                )
            """)
            print("✅ Table 'classe' créée")
            
            # Table salle
            db.execute("""
                CREATE TABLE IF NOT EXISTS salle (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT UNIQUE NOT NULL,
                    nom TEXT,
                    capacite INTEGER,
                    type_salle TEXT DEFAULT 'amphitheatre',
                    equipements TEXT,
                    batiment TEXT,
                    etage INTEGER
                )
            """)
            print("✅ Table 'salle' créée")
            
            # Table matiere
            db.execute("""
                CREATE TABLE IF NOT EXISTS matiere (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    code TEXT UNIQUE,
                    description TEXT,
                    coefficient REAL DEFAULT 1.0,
                    volume_horaire INTEGER,
                    filiere_id INTEGER,
                    FOREIGN KEY(filiere_id) REFERENCES filiere(id)
                )
            """)
            print("✅ Table 'matiere' créée")
            
            # Table examen
            db.execute("""
                CREATE TABLE IF NOT EXISTS examen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    classe_id INTEGER,
                    date_examen TEXT NOT NULL,
                    heure_debut TEXT,
                    heure_fin TEXT,
                    salle_id INTEGER,
                    type_examen TEXT DEFAULT 'controle',
                    coefficient REAL DEFAULT 1.0,
                    duree_minutes INTEGER,
                    FOREIGN KEY(matiere_id) REFERENCES matiere(id),
                    FOREIGN KEY(classe_id) REFERENCES classe(id),
                    FOREIGN KEY(salle_id) REFERENCES salle(id)
                )
            """)
            print("✅ Table 'examen' créée")
            
            # Table bulletin
            db.execute("""
                CREATE TABLE IF NOT EXISTS bulletin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_etudiant INTEGER NOT NULL,
                    classe_id INTEGER,
                    filiere_id INTEGER,
                    periode TEXT,
                    annee_scolaire TEXT,
                    moyenne_generale REAL,
                    rang INTEGER,
                    appreciation TEXT,
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(id_etudiant) REFERENCES etudiant(id),
                    FOREIGN KEY(classe_id) REFERENCES classe(id),
                    FOREIGN KEY(filiere_id) REFERENCES filiere(id)
                )
            """)
            print("✅ Table 'bulletin' créée")
            
            # Créer les index
            print("\n📊 Création des index...")
            try:
                db.execute("CREATE INDEX IF NOT EXISTS idx_etudiant_filiere ON etudiant(filiere_id)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_etudiant_classe ON etudiant(classe_id)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_professeur_filiere ON professeur(filiere_id)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_note_etudiant ON note(id_etudiant)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_note_matiere ON note(id_matiere)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_absence_etudiant ON absence(id_etudiant)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_absence_date ON absence(date_absence)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_cours_professeur ON cours(professeur_id)")
                db.execute("CREATE INDEX IF NOT EXISTS idx_cours_classe ON cours(classe_id)")
                print("✅ Index créés")
            except Exception as e:
                print(f"⚠️  Erreur lors de la création des index: {e}")
            
            db.commit()
            
            print("\n" + "=" * 60)
            print("✅ MIGRATION TERMINÉE AVEC SUCCÈS!")
            print("=" * 60)
            print("\n📋 15 tables disponibles:")
            print("   1. administrateur")
            print("   2. filiere")
            print("   3. departement")
            print("   4. professeur")
            print("   5. professeur_auth")
            print("   6. classe")
            print("   7. etudiant")
            print("   8. etudiant_auth")
            print("   9. matiere")
            print("   10. cours")
            print("   11. salle")
            print("   12. note")
            print("   13. absence")
            print("   14. examen")
            print("   15. bulletin")
            
        except Exception as e:
            db.rollback()
            print(f"\n❌ Erreur lors de la migration: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    migrate_to_15_tables()
