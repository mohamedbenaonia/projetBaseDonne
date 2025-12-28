from flask import Blueprint, request, jsonify
from database.db import db
from models.administrateur import Administrateur

administrateur_bp = Blueprint("administrateur_bp", __name__)

# CREATE
@administrateur_bp.route("/administrateurs", methods=["POST"])
def create_administrateur():
    data = request.json
    administrateur = Administrateur(username=data["username"], password=data["password"])
    db.session.add(administrateur)
    db.session.commit()
    return jsonify({"message": "Administrateur ajouté avec succès"}), 201

# READ ALL
@administrateur_bp.route("/administrateurs", methods=["GET"])
def get_all_administrateurs():
    administrateurs = Administrateur.query.all()
    return jsonify([
        {"id": a.id, "username": a.username} for a in administrateurs
    ])

# READ ONE
@administrateur_bp.route("/administrateurs/<int:id>", methods=["GET"])
def get_administrateur(id):
    a = Administrateur.query.get_or_404(id)
    return jsonify({"id": a.id, "username": a.username})

# UPDATE
@administrateur_bp.route("/administrateurs/<int:id>", methods=["PUT"])
def update_administrateur(id):
    a = Administrateur.query.get_or_404(id)
    data = request.json
    a.username = data["username"]
    a.password = data["password"]
    db.session.commit()
    return jsonify({"message": "Administrateur modifié avec succès"})

# DELETE
@administrateur_bp.route("/administrateurs/<int:id>", methods=["DELETE"])
def delete_administrateur(id):
    a = Administrateur.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": "Administrateur supprimé avec succès"})
