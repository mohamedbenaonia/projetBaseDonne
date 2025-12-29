class Config:
    SECRET_KEY = "ma_clef_secrete"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"  # ← fichier SQLite local
    SQLALCHEMY_TRACK_MODIFICATIONS = False       # pour éviter un avertissement
