from flask import Flask, render_template
from config import Config
from database.db import db
from routes.api import register_all_blueprints

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

register_all_blueprints(app)

@app.route("/")
def home():
    return render_template("index.html", titlepage="Accueil", stylefile="style")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # crée toutes les tables définies dans models
    app.run(debug=True)
