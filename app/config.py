"""
app/config.py — Configuration Classes
=======================================
Why this file exists:
    Centralizes ALL configuration in one place. Each class represents an
    environment (dev / prod / test). This avoids scattering magic strings
    like database URIs and secret keys across multiple files.

    Config values are loaded from environment variables (via python-dotenv)
    with sensible defaults for local development.
"""

import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()


class BaseConfig:
    """Shared configuration across all environments."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── Mistral AI ──────────────────────────────────────
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY', '')
    MISTRAL_MODEL = 'mistral-large-latest'

    # ── Speech Settings ─────────────────────────────────
    TTS_AUDIO_DIR = os.path.join('app', 'static', 'audio')
    SPEECH_LANGUAGE = 'en'


class DevelopmentConfig(BaseConfig):
    """Local development — debug ON, SQLite in instance/."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///app.db'
    )


class ProductionConfig(BaseConfig):
    """Production — debug OFF, stricter security."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


class TestingConfig(BaseConfig):
    """Testing — in-memory SQLite, no CSRF."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# ── Config Map ──────────────────────────────────────────
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
