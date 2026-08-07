"""
app/models/conversation.py — Conversation & Message Models
============================================================
Why this file exists:
    Persists AI chat history in SQLite. Each Conversation belongs to a User
    and contains multiple Messages (user prompts + AI responses). This lets
    the dashboard show conversation history, and the Mistral service can
    replay context for multi-turn conversations.
"""

from datetime import datetime, timezone
from ..extensions import db


class Conversation(db.Model):
    """A chat session between a user and the AI."""

    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), default='New Conversation')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ───────────────────────────────────
    messages = db.relationship(
        'Message', backref='conversation', lazy='dynamic',
        order_by='Message.created_at',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'message_count': self.messages.count(),
        }

    def __repr__(self):
        return f'<Conversation {self.id}: {self.title}>'


class Message(db.Model):
    """A single message within a conversation."""

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey('conversations.id'), nullable=False
    )
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    audio_path = db.Column(db.String(300), nullable=True)  # TTS audio file path
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'audio_path': self.audio_path,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<Message {self.role}: {self.content[:30]}...>'
