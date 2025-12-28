from flask import Flask, app
from config import Config
from database.db import db
# Importer la fonction d'enregistrement des blueprints principaux
from routes.api import register_all_blueprints

# Charger la configuration
app.config.from_object(Config)

# Lier Flask à la base de données
db.init_app(app)

# Enregistrer les blueprints principaux
register_all_blueprints(app)

@app.route("/")
def home():
    return "Backend Gestion École OK"

# Créer les tables au démarrage
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ← crée les 15 tables
    app.run(debug=True)



