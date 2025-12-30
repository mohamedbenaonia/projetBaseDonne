from flask import Flask, render_template
from config import Config
from database.db import get_db, close_db
from routes.api import register_all_blueprints

app = Flask(__name__)
app.config.from_object(Config)

register_all_blueprints(app)

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route("/")
def home():
    return render_template("index.html", titlepage="Accueil", stylefile="style")

def init_db():
    db = get_db()
    with open("schema.sql", encoding="utf-8") as f:
        db.executescript(f.read())

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
