# 🔧 Guide de Résolution des Problèmes

## Problème 1 : Les étudiants ne s'affichent pas chez les professeurs

### Cause
Le professeur ne voit que les étudiants qui sont dans **la même filière** que lui.

### Solution

**Option 1 : Vérifier les filières**
1. Connectez-vous en tant qu'administrateur
2. Allez dans le dashboard administrateur
3. Vérifiez la filière du professeur et la filière de l'étudiant
4. Ils doivent avoir la **même filière_id**

**Option 2 : Créer un nouveau compte avec la même filière**
1. Lors de la création du compte étudiant, choisissez la **même filière** que le professeur
2. Lors de la création du compte professeur, choisissez la **même filière** que l'étudiant

**Option 3 : Vérifier dans la base de données**
Exécutez ce script pour voir les correspondances :
```bash
python -c "from app import app; from database.db import get_db; exec(open('check_filiere.py').read())"
```

## Problème 2 : Impossible de créer un compte administrateur

### Vérifications

1. **Le formulaire est-il correctement rempli ?**
   - Nom d'utilisateur : requis
   - Mot de passe : minimum 6 caractères
   - Confirmation du mot de passe : doit correspondre

2. **Vérifier la console du navigateur (F12)**
   - Ouvrez les outils de développement (F12)
   - Allez dans l'onglet "Console"
   - Essayez de créer un compte
   - Regardez les erreurs affichées

3. **Vérifier les logs du serveur**
   - Regardez la console où l'application Flask tourne
   - Cherchez les erreurs

### Solution rapide

Si le problème persiste, créez un administrateur directement via Python :
```python
from app import app
from database.db import get_db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

with app.app_context():
    db = get_db()
    username = "admin"
    password = hash_password("admin123")
    db.execute("INSERT OR IGNORE INTO administrateur (username, password) VALUES (?, ?)", 
               (username, password))
    db.commit()
    print("✅ Administrateur créé : admin / admin123")
```

## Vérification rapide

Pour vérifier que tout fonctionne :

1. **Vérifier les filières** :
```bash
python init_filieres.py
```

2. **Vérifier la structure de la base de données** :
```bash
python migrate_to_15_tables.py
```

3. **Créer des données de test** :
```bash
python init_data.py
```

## Contact

Si les problèmes persistent, vérifiez :
- Que la base de données existe (`database/database.db`)
- Que toutes les tables sont créées (15 tables)
- Que les filières existent (au moins 1 filière)
- Les logs d'erreur dans la console du navigateur et du serveur

