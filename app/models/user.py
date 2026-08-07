"""
app/models/user.py — User Model
=================================
Why this file exists:
    Defines the `User` table in SQLite via SQLAlchemy ORM. Handles
    authentication fields (email, password hash) and integrates with
    Flask-Login for session management. Kept in its own file so the
    user schema can evolve independently of career/conversation models.
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..extensions import db, login_manager


class User(UserMixin, db.Model):
    """Registered user account."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # ── Relationships ───────────────────────────────────
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic')

    # ── Password Helpers ────────────────────────────────
    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login callback: load user by primary key."""
    return User.query.get(int(user_id))
