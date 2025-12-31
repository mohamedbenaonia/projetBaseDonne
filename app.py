from flask import Flask
from database.db import get_db, close_db
from config import Config
from routes.api import register_all_blueprints

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

def init_db():
    db = get_db()
    with open("schema.sql", encoding="utf-8") as f:
        db.executescript(f.read())

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

# Enregistrer toutes les routes
register_all_blueprints(app)

# Route par défaut vers la page de connexion
@app.route("/")
def index():
    from flask import redirect, url_for
    return redirect(url_for("auth_bp.login_page"))

if __name__ == "__main__":
    with app.app_context():
        init_db()  # crée toutes les tables à partir de schema.sql
    app.run(debug=True)
