"""
app/utils/validators.py — Input Validation Functions
======================================================
Why this file exists:
    Centralizes input validation logic so routes and services can validate
    user input consistently. Better than scattering regex checks and
    length limits across multiple route files.
"""

import re


def validate_email(email):
    """
    Validate email format.

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not email or not email.strip():
        return False, 'Email is required.'

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, 'Invalid email format.'

    return True, None


def validate_password(password, min_length=6):
    """
    Validate password strength.

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not password:
        return False, 'Password is required.'

    if len(password) < min_length:
        return False, f'Password must be at least {min_length} characters.'

    return True, None


def validate_username(username, min_length=3, max_length=80):
    """
    Validate username format.

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not username or not username.strip():
        return False, 'Username is required.'

    if len(username) < min_length:
        return False, f'Username must be at least {min_length} characters.'

    if len(username) > max_length:
        return False, f'Username must be at most {max_length} characters.'

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, 'Username can only contain letters, numbers, and underscores.'

    return True, None
