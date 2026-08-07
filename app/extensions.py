"""
app/extensions.py — Flask Extension Instances
===============================================
Why this file exists:
    Extensions (SQLAlchemy, Migrate, LoginManager) are instantiated HERE
    but NOT bound to any app yet. The app factory calls `ext.init_app(app)`
    later. This two-step pattern prevents circular imports:

        models.py  →  needs `db` from extensions.py
        __init__.py → needs models + extensions
        extensions.py → needs NEITHER (no app, no models)

    Without this file, you'd get circular import errors the moment your
    project grows beyond a single file.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# ── Database ORM ────────────────────────────────────────
db = SQLAlchemy()

# ── Database Migrations (Alembic) ───────────────────────
migrate = Migrate()

# ── User Session Management ────────────────────────────
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
