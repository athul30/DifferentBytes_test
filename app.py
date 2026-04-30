import os
from flask import Flask, jsonify
from models import db
from routes.details import details_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)


    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/testdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secret-ecommerce-key-2026")

    
    db.init_app(app)


    app.register_blueprint(details_bp)

    
    with app.app_context():
        try:
            db.create_all()
            print("✓ Tables created successfully")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
