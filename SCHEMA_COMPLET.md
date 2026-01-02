# 📊 Schéma de Base de Données Complet - 15 Tables

## Vue d'ensemble

Le système de gestion universitaire comprend maintenant **15 tables** interconnectées pour une gestion complète et détaillée.

## Liste des Tables

### 1. **administrateur**
Gestion des administrateurs du système
- `id` (PK)
- `username` (UNIQUE)
- `password`
- `date_creation`

### 2. **filiere**
Filières d'études
- `id` (PK)
- `nom` (UNIQUE)
- `description`
- `responsable_id` (FK → professeur)
- `date_creation`

### 3. **departement**
Départements universitaires
- `id` (PK)
- `nom` (UNIQUE)
- `description`
- `chef_departement_id` (FK → professeur)
- `date_creation`

### 4. **professeur**
Informations des professeurs
- `id` (PK)
- `nom`, `prenom`
- `email`, `telephone`
- `filiere_id` (FK → filiere)
- `departement_id` (FK → departement)
- `specialite`
- `date_embauche`
- `statut`

### 5. **professeur_auth**
Authentification des professeurs
- `id` (PK)
- `professeur_id` (FK → professeur, UNIQUE)
- `email` (UNIQUE)
- `password`
- `date_creation`

### 6. **classe**
Classes/Groupes d'étudiants
- `id` (PK)
- `nom`
- `niveau`
- `filiere_id` (FK → filiere)
- `professeur_principal_id` (FK → professeur)
- `capacite_max`
- `annee_scolaire`

### 7. **etudiant**
Informations des étudiants
- `id` (PK)
- `nom`, `prenom`
- `email`, `telephone`
- `date_naissance`
- `adresse`
- `filiere_id` (FK → filiere)
- `classe_id` (FK → classe)
- `numero_etudiant` (UNIQUE)
- `date_inscription`
- `statut`

### 8. **etudiant_auth**
Authentification des étudiants
- `id` (PK)
- `etudiant_id` (FK → etudiant, UNIQUE)
- `email` (UNIQUE)
- `password`
- `date_creation`

### 9. **matiere**
Matières enseignées
- `id` (PK)
- `nom`
- `code` (UNIQUE)
- `description`
- `coefficient`
- `volume_horaire`
- `filiere_id` (FK → filiere)

### 10. **cours**
Cours programmés
- `id` (PK)
- `nom`
- `matiere_id` (FK → matiere)
- `professeur_id` (FK → professeur)
- `classe_id` (FK → classe)
- `filiere_id` (FK → filiere)
- `salle_id` (FK → salle)
- `jour_semaine`
- `heure_debut`, `heure_fin`

### 11. **salle**
Salles de cours
- `id` (PK)
- `numero` (UNIQUE)
- `nom`
- `capacite`
- `type_salle`
- `equipements`
- `batiment`
- `etage`

### 12. **note**
Notes des étudiants
- `id` (PK)
- `id_etudiant` (FK → etudiant)
- `id_cours` (FK → cours)
- `id_matiere` (FK → matiere)
- `id_professeur` (FK → professeur)
- `valeur`
- `type_note`
- `coefficient`
- `commentaire`
- `date_note`

### 13. **absence**
Absences des étudiants
- `id` (PK)
- `id_etudiant` (FK → etudiant)
- `id_cours` (FK → cours)
- `id_professeur` (FK → professeur)
- `date_absence`
- `heure_debut`, `heure_fin`
- `justifiee`
- `motif`
- `date_justification`

### 14. **examen**
Examens programmés
- `id` (PK)
- `nom`
- `matiere_id` (FK → matiere)
- `classe_id` (FK → classe)
- `date_examen`
- `heure_debut`, `heure_fin`
- `salle_id` (FK → salle)
- `type_examen`
- `coefficient`
- `duree_minutes`

### 15. **bulletin**
Bulletins de notes
- `id` (PK)
- `id_etudiant` (FK → etudiant)
- `classe_id` (FK → classe)
- `filiere_id` (FK → filiere)
- `periode`
- `annee_scolaire`
- `moyenne_generale`
- `rang`
- `appreciation`
- `date_creation`

## Relations Principales

```
filiere (1) ──< (N) professeur
filiere (1) ──< (N) etudiant
filiere (1) ──< (N) classe
filiere (1) ──< (N) matiere

departement (1) ──< (N) professeur

classe (1) ──< (N) etudiant
classe (1) ──< (N) cours
classe (1) ──< (N) examen

professeur (1) ──< (N) cours
professeur (1) ──< (N) note
professeur (1) ──< (N) absence

matiere (1) ──< (N) cours
matiere (1) ──< (N) note
matiere (1) ──< (N) examen

salle (1) ──< (N) cours
salle (1) ──< (N) examen

etudiant (1) ──< (N) note
etudiant (1) ──< (N) absence
etudiant (1) ──< (N) bulletin

cours (1) ──< (N) note
cours (1) ──< (N) absence
```

## Index Créés

Pour optimiser les performances :
- `idx_etudiant_filiere` sur `etudiant(filiere_id)`
- `idx_etudiant_classe` sur `etudiant(classe_id)`
- `idx_professeur_filiere` sur `professeur(filiere_id)`
- `idx_note_etudiant` sur `note(id_etudiant)`
- `idx_note_matiere` sur `note(id_matiere)`
- `idx_absence_etudiant` sur `absence(id_etudiant)`
- `idx_absence_date` sur `absence(date_absence)`
- `idx_cours_professeur` sur `cours(professeur_id)`
- `idx_cours_classe` sur `cours(classe_id)`

## Fonctionnalités Ajoutées

### Nouvelles Entités
- ✅ **Classes** : Groupement d'étudiants par niveau
- ✅ **Matières** : Matières enseignées avec coefficients
- ✅ **Salles** : Gestion des salles de cours
- ✅ **Examens** : Planification des examens
- ✅ **Bulletins** : Génération automatique des bulletins
- ✅ **Départements** : Organisation par départements

### Améliorations
- ✅ Informations détaillées des étudiants (téléphone, adresse, date de naissance)
- ✅ Informations détaillées des professeurs (spécialité, date d'embauche)
- ✅ Gestion des absences justifiées/non justifiées
- ✅ Types de notes (contrôle, examen, TP, etc.)
- ✅ Coefficients pour les notes et matières
- ✅ Emploi du temps avec horaires précis
- ✅ Statuts pour étudiants et professeurs

