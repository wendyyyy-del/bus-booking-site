from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Booking, Bus


bp = Blueprint("profile", __name__)

@bp.route("/", methods=["GET", "OPTIONS"])
@jwt_required(optional=True)  # Optional so preflight doesn't fail
def get_profile():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight"}), 200

    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    bookings = Booking.query.filter_by(user_id=user.id).all()
    booking_data = []
    for b in bookings:
        bus = Bus.query.get(b.bus_id)
        booking_data.append({
            "bus": bus.name,
            "route": bus.route,
            "image_url": bus.image_url
        })

    return jsonify({
        "id": user.id,
        "email": user.email,
        "bookings": booking_data
    })
