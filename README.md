# 🎓 Plateforme Universitaire - Système de Gestion

Une plateforme moderne et stylée pour la gestion des étudiants, professeurs, notes et absences.

## ✨ Fonctionnalités

### 🔐 Système d'authentification
- Page de connexion moderne avec sélection du type d'utilisateur
- Connexion sécurisée pour étudiants, professeurs et administrateurs
- Gestion de session

### 👨‍🏫 Interface Professeur
- Dashboard avec statistiques
- **Gestion des notes** :
  - Choisir un étudiant
  - Choisir une matière
  - Ajouter une note (sur 20)
  - Ajouter un commentaire
- **Gestion des absences** :
  - Choisir un étudiant
  - Choisir une matière
  - Ajouter une absence avec date
  - Voir le taux d'absence par matière

### 👨‍🎓 Interface Étudiant
- Dashboard personnel
- **Consultation des notes** :
  - Choisir une matière
  - Voir toutes les notes avec commentaires
  - Voir le nom du professeur
  - Calcul automatique de la moyenne
- **Consultation des absences** :
  - Choisir une matière
  - Voir toutes les absences
  - Voir le taux d'absence par matière
  - Voir qui a enregistré l'absence

### 👤 Interface Administrateur
- Vue d'ensemble complète de la plateforme
- Statistiques globales (étudiants, professeurs, cours, notes, absences)
- Consultation de toutes les données :
  - Liste des étudiants
  - Liste des professeurs
  - Liste des cours
  - Notes récentes
  - Absences récentes

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.7+
- Flask

### Installation

1. Installez les dépendances :
```bash
pip install flask
```

2. Initialisez la base de données :
```bash
python app.py
```
(Cela créera automatiquement les tables)

3. Créez des données de test (optionnel) :
```bash
python init_data.py
```

### Démarrage

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 👥 Comptes de Test

Après avoir exécuté `init_data.py`, vous pouvez vous connecter avec :

### Administrateur
- **Username** : `admin`
- **Password** : `admin123`

### Professeur
- **Email** : `prof@example.com`
- **Password** : `prof123`

### Étudiant
- **Email** : `sophie@example.com`
- **Password** : `etudiant123`

## 📁 Structure du Projet

```
mohamedbenaonia/
├── app.py                 # Application principale
├── config.py              # Configuration
├── schema.sql             # Schéma de base de données
├── init_data.py           # Script d'initialisation des données de test
├── controllers/           # Contrôleurs (logique métier)
│   ├── auth_controller.py
│   ├── administrateur_controller.py
│   ├── etudiant_controller.py
│   ├── professeur_controller.py
│   ├── note_controller.py
│   └── absence_controller.py
├── routes/
│   └── api.py             # Enregistrement des routes
├── database/
│   ├── db.py              # Connexion à la base de données
│   └── database.db        # Base de données SQLite
├── templates/             # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── professeur_dashboard.html
│   ├── etudiant_dashboard.html
│   └── administrateur_dashboard.html
└── static/
    └── style.css          # Styles CSS modernes
```

## 🎨 Design

La plateforme utilise un design moderne avec :
- Interface responsive
- Couleurs modernes et gradients
- Animations fluides
- Cartes et badges stylisés
- Tableaux interactifs

## 🔒 Sécurité

- Mots de passe hashés (SHA-256)
- Gestion de session Flask
- Protection des routes par type d'utilisateur
- Validation des données

## 📝 Notes

- La base de données est SQLite (fichier local)
- Les mots de passe sont hashés avec SHA-256
- Les sessions sont gérées par Flask
- Le design est entièrement responsive

## 🛠️ Technologies Utilisées

- **Backend** : Flask (Python)
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3, JavaScript
- **Authentification** : Sessions Flask

## 📝 Licence

Ce projet est un projet éducatif

