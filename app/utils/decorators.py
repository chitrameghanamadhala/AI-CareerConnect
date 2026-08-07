"""
app/utils/decorators.py — Custom Decorators
==============================================
Why this file exists:
    Reusable function decorators that wrap route handlers. Keeps
    cross-cutting concerns (role checks, rate limiting, admin access)
    out of route logic. Apply with @decorator syntax.
"""

from functools import wraps
from flask import abort, jsonify, request
from flask_login import current_user


def admin_required(f):
    """
    Restrict a route to admin users only.

    Usage:
        @app.route('/admin')
        @login_required
        @admin_required
        def admin_panel():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not getattr(current_user, 'is_admin', False):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def json_required(f):
    """
    Ensure the request body contains valid JSON.

    Usage:
        @api_bp.route('/data', methods=['POST'])
        @json_required
        def receive_data():
            data = request.get_json()
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function
