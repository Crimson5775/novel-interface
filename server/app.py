from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from .routes.auth import auth
from .routes.admin import admin
from .routes.novels import novels
from .routes.static_routes import static_routes
from .commands import create_admin
from .config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../')
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app)
    JWTManager(app)
    db.init_app(app)

    # Create upload folders if they don't exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'covers'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'chapters'), exist_ok=True)

    # Register blueprints
    app.register_blueprint(static_routes)  # Register this first
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(admin, url_prefix='/api/admin')
    app.register_blueprint(novels, url_prefix='/api/novels')

    # Register commands
    app.cli.add_command(create_admin)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
