from flask import Blueprint, request, jsonify
from models import db, Details

details_bp = Blueprint("details", __name__)


@details_bp.route("/details", methods=["POST"])
def create_details():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "Name, email, and message are required."}), 400

    new_details = Details(name=name, email=email, message=message)
    db.session.add(new_details)
    db.session.commit()

    return jsonify(new_details.to_dict()), 201