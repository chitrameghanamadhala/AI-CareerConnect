"""
app/utils/helpers.py — Miscellaneous Helper Functions
=======================================================
Why this file exists:
    Small, reusable utility functions that don't belong to any specific
    service or route. Examples: date formatting, string truncation,
    slug generation. Prevents scattering one-liners across the codebase.
"""

import re
from datetime import datetime, timezone


def time_ago(dt):
    """
    Convert a datetime to a human-readable "time ago" string.

    Args:
        dt: A datetime object (assumed UTC).

    Returns:
        str: e.g., "2 hours ago", "3 days ago"
    """
    now = datetime.now(timezone.utc)
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    else:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days != 1 else ""} ago'


def truncate(text, length=100, suffix='...'):
    """Truncate text to a maximum length."""
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text
