"""
app/__init__.py — Application Factory
=======================================
Why this file exists:
    The App Factory pattern (`create_app()`) lets us create multiple app
    instances with different configs (dev, test, prod) without import
    side-effects. Flask officially recommends this pattern for any
    project beyond a single-file app.

    This file wires together:
    - Configuration loading
    - Extension initialization (DB, migrations, login manager)
    - Blueprint registration (routes)
    - Database table creation
"""

from flask import Flask
from .config import config_map
from .extensions import db, migrate, login_manager


def create_app(config_name='development'):
    """
    Factory function that builds and returns a configured Flask app.

    Args:
        config_name: One of 'development', 'production', 'testing'.
                     Defaults to 'development'.
    """
    app = Flask(__name__, instance_relative_config=True)

    # ── Load Configuration ──────────────────────────────
    app.config.from_object(config_map.get(config_name, config_map['development']))

    # ── Initialize Extensions ───────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ── Register Blueprints ─────────────────────────────
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.career import career_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # ── Create DB Tables ────────────────────────────────
    with app.app_context():
        from . import models  # noqa: F401 — triggers model registration
        db.create_all()

    return app
