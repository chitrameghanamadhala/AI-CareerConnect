"""
run.py — Application Entry Point
=================================
Thin launcher that imports the app factory and starts the Flask dev server.
Keeps the `app` package cleanly importable without side-effects.

Usage:
    python run.py
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
