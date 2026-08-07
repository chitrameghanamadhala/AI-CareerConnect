"""
app/services/__init__.py — Services Package
=============================================
Why this file exists:
    Makes `services/` a Python package. Services contain business logic
    that is decoupled from Flask routes — making them testable, reusable,
    and swappable (e.g., swap Mistral for OpenAI without touching routes).
"""
