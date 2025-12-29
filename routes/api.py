

from controllers.etudiant_controller import etudiant_bp
from controllers.professeur_controller import professeur_bp
'''from controllers.absence_controller import absence_bp
from controllers.bulletin_controller import bulletin_bp
from controllers.classe_controller import classe_bp
from controllers.cours_controller import cours_bp
from controllers.emploi_temps_controller import emploi_temps_bp
from controllers.examen_controller import examen_bp
from controllers.inscription_controller import inscription_bp
from controllers.matiere_controller import matiere_bp
from controllers.note_controller import note_bp
from controllers.salle_controller import salle_bp
from controllers.departement_controller import departement_bp
from controllers.prof_departement_controller import prof_departement_bp'''
from controllers.administrateur_controller import administrateur_bp

def register_all_blueprints(app):
	app.register_blueprint(etudiant_bp)
	app.register_blueprint(professeur_bp)
	'''app.register_blueprint(absence_bp)
	app.register_blueprint(bulletin_bp)
	app.register_blueprint(classe_bp)
	app.register_blueprint(cours_bp)
	app.register_blueprint(emploi_temps_bp)
	app.register_blueprint(examen_bp)
	app.register_blueprint(inscription_bp)
	app.register_blueprint(matiere_bp)
	app.register_blueprint(note_bp)
	app.register_blueprint(salle_bp)
	app.register_blueprint(departement_bp)
	app.register_blueprint(prof_departement_bp)'''
	app.register_blueprint(administrateur_bp)
