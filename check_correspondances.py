"""
Script pour vérifier les correspondances entre professeurs et étudiants
"""
from app import app
from database.db import get_db

with app.app_context():
    db = get_db()
    
    print("=" * 60)
    print("VÉRIFICATION DES CORRESPONDANCES PROFESSEUR-ÉTUDIANT")
    print("=" * 60)
    
    # Afficher tous les professeurs avec leurs étudiants
    professeurs = db.execute("""
        SELECT professeur.*, filiere.nom as filiere_nom 
        FROM professeur 
        LEFT JOIN filiere ON professeur.filiere_id = filiere.id
    """).fetchall()
    
    print(f"\n👨‍🏫 {len(professeurs)} professeur(s) trouvé(s):\n")
    
    for prof in professeurs:
        print(f"📌 Professeur: {prof['nom']} {prof['prenom']} (ID: {prof['id']})")
        print(f"   Filière: {prof['filiere_id']} - {prof['filiere_nom'] if prof['filiere_nom'] else 'AUCUNE'}")
        
        if prof['filiere_id']:
            # Chercher les étudiants dans la même filière
            etudiants = db.execute(
                "SELECT * FROM etudiant WHERE filiere_id = ?", 
                (prof['filiere_id'],)
            ).fetchall()
            
            if etudiants:
                print(f"   ✅ {len(etudiants)} étudiant(s) dans la même filière:")
                for e in etudiants:
                    print(f"      - {e['nom']} {e['prenom']} (ID: {e['id']}, Email: {e['email']})")
            else:
                print(f"   ❌ Aucun étudiant dans cette filière")
                # Afficher tous les étudiants pour référence
                tous_etudiants = db.execute("""
                    SELECT etudiant.*, filiere.nom as filiere_nom 
                    FROM etudiant 
                    LEFT JOIN filiere ON etudiant.filiere_id = filiere.id
                """).fetchall()
                if tous_etudiants:
                    print(f"   💡 Étudiants disponibles dans d'autres filières:")
                    for e in tous_etudiants:
                        print(f"      - {e['nom']} {e['prenom']} (Filière: {e['filiere_id']} - {e['filiere_nom'] if e['filiere_nom'] else 'Aucune'})")
        else:
            print(f"   ⚠️  Ce professeur n'a pas de filière assignée!")
        
        print()
    
    print("=" * 60)
    print("💡 SOLUTION:")
    print("=" * 60)
    print("Pour qu'un professeur voie un étudiant:")
    print("1. Le professeur et l'étudiant doivent avoir la MÊME filiere_id")
    print("2. La filiere_id ne doit pas être NULL")
    print("\nSi les filières ne correspondent pas:")
    print("- Créez un nouveau compte avec la même filière")
    print("- Ou modifiez la filière dans la base de données")

