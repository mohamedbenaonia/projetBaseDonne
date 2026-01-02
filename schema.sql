-- ============================================
-- SCHÉMA DE BASE DE DONNÉES COMPLET (15 TABLES)
-- Plateforme Universitaire - Système de Gestion
-- ============================================

-- 1. Table Administrateur
CREATE TABLE IF NOT EXISTS administrateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 2. Table Filière (sans référence à professeur pour éviter dépendance circulaire)
CREATE TABLE IF NOT EXISTS filiere (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL,
    description TEXT,
    responsable_id INTEGER,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 3. Table Département
CREATE TABLE IF NOT EXISTS departement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL,
    description TEXT,
    chef_departement_id INTEGER,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(chef_departement_id) REFERENCES professeur(id)
);

-- 4. Table Professeur
CREATE TABLE IF NOT EXISTS professeur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT,
    telephone TEXT,
    filiere_id INTEGER,
    departement_id INTEGER,
    specialite TEXT,
    date_embauche TEXT,
    statut TEXT DEFAULT 'actif',
    FOREIGN KEY(filiere_id) REFERENCES filiere(id),
    FOREIGN KEY(departement_id) REFERENCES departement(id)
);

-- 5. Table Authentification Professeur
CREATE TABLE IF NOT EXISTS professeur_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    professeur_id INTEGER UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(professeur_id) REFERENCES professeur(id)
);

-- 6. Table Classe
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
);

-- 7. Table Étudiant
CREATE TABLE IF NOT EXISTS etudiant (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT,
    telephone TEXT,
    date_naissance TEXT,
    adresse TEXT,
    filiere_id INTEGER,
    classe_id INTEGER,
    numero_etudiant TEXT UNIQUE,
    date_inscription TEXT DEFAULT CURRENT_TIMESTAMP,
    statut TEXT DEFAULT 'actif',
    FOREIGN KEY(filiere_id) REFERENCES filiere(id),
    FOREIGN KEY(classe_id) REFERENCES classe(id)
);

-- 8. Table Authentification Étudiant
CREATE TABLE IF NOT EXISTS etudiant_auth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(etudiant_id) REFERENCES etudiant(id)
);

-- 9. Table Salle (créée avant cours car cours référence salle)
CREATE TABLE IF NOT EXISTS salle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    nom TEXT,
    capacite INTEGER,
    type_salle TEXT DEFAULT 'amphitheatre',
    equipements TEXT,
    batiment TEXT,
    etage INTEGER
);

-- 10. Table Matière
CREATE TABLE IF NOT EXISTS matiere (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    code TEXT UNIQUE,
    description TEXT,
    coefficient REAL DEFAULT 1.0,
    volume_horaire INTEGER,
    filiere_id INTEGER,
    FOREIGN KEY(filiere_id) REFERENCES filiere(id)
);

-- 11. Table Cours
CREATE TABLE IF NOT EXISTS cours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    matiere_id INTEGER NOT NULL,
    professeur_id INTEGER NOT NULL,
    classe_id INTEGER,
    filiere_id INTEGER,
    salle_id INTEGER,
    jour_semaine TEXT,
    heure_debut TEXT,
    heure_fin TEXT,
    FOREIGN KEY(matiere_id) REFERENCES matiere(id),
    FOREIGN KEY(professeur_id) REFERENCES professeur(id),
    FOREIGN KEY(classe_id) REFERENCES classe(id),
    FOREIGN KEY(filiere_id) REFERENCES filiere(id),
    FOREIGN KEY(salle_id) REFERENCES salle(id)
);

-- 12. Table Note
CREATE TABLE IF NOT EXISTS note (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_etudiant INTEGER NOT NULL,
    id_cours INTEGER NOT NULL,
    id_matiere INTEGER NOT NULL,
    id_professeur INTEGER NOT NULL,
    valeur REAL NOT NULL,
    type_note TEXT DEFAULT 'controle',
    coefficient REAL DEFAULT 1.0,
    commentaire TEXT,
    date_note TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_etudiant) REFERENCES etudiant(id),
    FOREIGN KEY(id_cours) REFERENCES cours(id),
    FOREIGN KEY(id_matiere) REFERENCES matiere(id),
    FOREIGN KEY(id_professeur) REFERENCES professeur(id)
);

-- 13. Table Absence
CREATE TABLE IF NOT EXISTS absence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_etudiant INTEGER NOT NULL,
    id_cours INTEGER NOT NULL,
    id_professeur INTEGER NOT NULL,
    date_absence TEXT NOT NULL,
    heure_debut TEXT,
    heure_fin TEXT,
    justifiee INTEGER DEFAULT 0,
    motif TEXT,
    date_justification TEXT,
    FOREIGN KEY(id_etudiant) REFERENCES etudiant(id),
    FOREIGN KEY(id_cours) REFERENCES cours(id),
    FOREIGN KEY(id_professeur) REFERENCES professeur(id)
);

-- 14. Table Examen
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
);

-- 15. Table Bulletin
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
);

-- ============================================
-- INDEX POUR OPTIMISATION
-- ============================================
CREATE INDEX IF NOT EXISTS idx_etudiant_filiere ON etudiant(filiere_id);
CREATE INDEX IF NOT EXISTS idx_etudiant_classe ON etudiant(classe_id);
CREATE INDEX IF NOT EXISTS idx_professeur_filiere ON professeur(filiere_id);
CREATE INDEX IF NOT EXISTS idx_note_etudiant ON note(id_etudiant);
CREATE INDEX IF NOT EXISTS idx_note_matiere ON note(id_matiere);
CREATE INDEX IF NOT EXISTS idx_absence_etudiant ON absence(id_etudiant);
CREATE INDEX IF NOT EXISTS idx_absence_date ON absence(date_absence);
CREATE INDEX IF NOT EXISTS idx_cours_professeur ON cours(professeur_id);
CREATE INDEX IF NOT EXISTS idx_cours_classe ON cours(classe_id);
