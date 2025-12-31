from controllers.auth_controller import auth_bp
from controllers.administrateur_controller import administrateur_bp
from controllers.etudiant_controller import etudiant_bp
from controllers.professeur_controller import professeur_bp
from controllers.classe_controller import classe_bp
from controllers.note_controller import note_bp
from controllers.bulletin_controller import bulletin_bp
from controllers.absence_controller import absence_bp
from controllers.examen_controller import examen_bp
from controllers.salle_controller import salle_bp
from controllers.matiere_controller import matiere_bp
from controllers.departement_controller import departement_bp

def register_all_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(administrateur_bp)
    app.register_blueprint(etudiant_bp)
    app.register_blueprint(professeur_bp)
    app.register_blueprint(classe_bp)
    app.register_blueprint(note_bp)
    app.register_blueprint(bulletin_bp)
    app.register_blueprint(absence_bp)
    app.register_blueprint(examen_bp)
    app.register_blueprint(salle_bp)
    app.register_blueprint(matiere_bp)
    app.register_blueprint(departement_bp)
