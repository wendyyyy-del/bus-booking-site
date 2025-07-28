from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    
    app.config.from_object("config.Config")


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS(app)
    
    if os.getenv("FLASK_ENV") == "production":
        
        CORS(
            app,
                resources={r"/api/*": {"origins": ["http://localhost:3000"]}},
            supports_credentials=True
        )
    else:
        
        CORS(
            app,
            resources={r"/api/*": {"origins": "*"}},
            supports_credentials=True
        )

    
    @jwt.unauthorized_loader
    def unauthorized(reason):
        return jsonify({"message": f"Unauthorized: {reason}"}), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({"message": f"Invalid token: {reason}"}), 422

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({"message": "Token expired"}), 401

    # register blueprints
    from app.routes import auth, buses, bookings, profile

    app.register_blueprint(auth.bp, url_prefix="/api/auth")
    app.register_blueprint(buses.bp, url_prefix="/api/buses")
    app.register_blueprint(bookings.bp, url_prefix="/api/bookings")
    app.register_blueprint(profile.bp, url_prefix="/api/profile")

    
    @app.route("/")
    def index():
        return jsonify({"message": "Bus Booking API is running"})

    return app
