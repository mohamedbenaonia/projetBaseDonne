from flask import Blueprint, request, jsonify, render_template
from database.db import get_db

administrateur_bp = Blueprint("administrateur_bp", __name__)

# CREATE
@administrateur_bp.route("/administrateurs", methods=["POST"])
def create_administrateur():
    data = request.json
    db = get_db()
    db.execute(
        "INSERT INTO administrateur (username, password) VALUES (?, ?)",
        (data["username"], data["password"])
    )
    db.commit()
    return jsonify({"message": "Administrateur ajouté avec succès"}), 201


# READ ALL
@administrateur_bp.route("/administrateurs", methods=["GET"])
def get_all_administrateurs():
    db = get_db()
    rows = db.execute(
        "SELECT id, username FROM administrateur"
    ).fetchall()
    return jsonify([dict(r) for r in rows])


# READ ONE
@administrateur_bp.route("/administrateurs/<int:id>", methods=["GET"])
def get_administrateur(id):
    db = get_db()
    row = db.execute(
        "SELECT id, username FROM administrateur WHERE id = ?",
        (id,)
    ).fetchone()

    if row is None:
        return jsonify({"error": "Administrateur non trouvé"}), 404

    return jsonify(dict(row))


# UPDATE
@administrateur_bp.route("/administrateurs/<int:id>", methods=["PUT"])
def update_administrateur(id):
    data = request.json
    db = get_db()
    cursor = db.execute(
        "UPDATE administrateur SET username = ?, password = ? WHERE id = ?",
        (data["username"], data["password"], id)
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Administrateur non trouvé"}), 404

    return jsonify({"message": "Administrateur modifié avec succès"})


# DELETE
@administrateur_bp.route("/administrateurs/<int:id>", methods=["DELETE"])
def delete_administrateur(id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM administrateur WHERE id = ?",
        (id,)
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Administrateur non trouvé"}), 404

    return jsonify({"message": "Administrateur supprimé avec succès"})


# PAGE HTML
@administrateur_bp.route("/page", methods=["GET"])
def administrateur_page():
    return render_template(
        "administrateur.html",
        stylefile="administrateur",
        titlepage="Administrateurs"
    )
