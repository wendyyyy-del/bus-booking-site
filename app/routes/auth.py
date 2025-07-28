from flask import Blueprint, request
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(email=data["email"]).first():
        return {"message": "User already exists"}, 400

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return {"message": "User registered"}

@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return {"message": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))
    return {"token": token, "user": {"id": user.id, "email": user.email}}
