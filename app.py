from flask import Flask, render_template
from config import Config
from database.db import db
from routes.api import register_all_blueprints

# Créer l'application Flask
app = Flask(__name__)  # ← obligatoire avant tout

# Charger la configuration
app.config.from_object(Config)

# Lier Flask à la base de données
db.init_app(app)

# Enregistrer les blueprints
register_all_blueprints(app)

@app.route("/")
def home():
    return render_template("index.html", titlepage="Home Page", stylefile="style")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # crée les tables
    app.run(debug=True)
