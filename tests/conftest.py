"""
tests/conftest.py — Pytest Fixtures
======================================
Why this file exists:
    Provides shared test fixtures (test app, test client, test DB).
    `conftest.py` is a special pytest file — fixtures defined here are
    automatically available to ALL test files without importing.

    Uses TestingConfig which gives an in-memory SQLite database, so
    tests are fast and don't touch the real database.
"""

import pytest
from app import create_app
from app.extensions import db as _db
from app.models.user import User


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    yield app


@pytest.fixture(scope='function')
def db(app):
    """Create a fresh database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def sample_user(db):
    """Create and return a sample user."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user
