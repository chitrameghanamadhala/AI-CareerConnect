"""
app/models/__init__.py — Model Package Initializer
====================================================
Why this file exists:
    Imports all models so SQLAlchemy discovers them when `db.create_all()`
    runs. Without these imports, tables won't be created because Python
    won't have loaded the model classes into memory.
"""

from .user import User  # noqa: F401
from .career import Career, Skill  # noqa: F401
from .conversation import Conversation, Message  # noqa: F401
