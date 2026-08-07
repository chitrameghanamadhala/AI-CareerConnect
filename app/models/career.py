"""
app/models/career.py — Career & Skill Models
==============================================
Why this file exists:
    Stores career/job data and associated skills in SQLite. The many-to-many
    relationship between Career and Skill uses an association table so one
    skill (e.g., "Python") can belong to multiple careers and vice versa.
    Separating this from user.py keeps domain boundaries clean.
"""

from datetime import datetime, timezone
from ..extensions import db


# ── Many-to-Many Association Table ──────────────────────
career_skills = db.Table(
    'career_skills',
    db.Column('career_id', db.Integer, db.ForeignKey('careers.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True),
)


class Career(db.Model):
    """A career path or job role with metadata."""

    __tablename__ = 'careers'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    avg_salary = db.Column(db.Float, nullable=True)
    growth_rate = db.Column(db.Float, nullable=True)  # percentage
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # ── Relationships ───────────────────────────────────
    skills = db.relationship(
        'Skill',
        secondary=career_skills,
        backref=db.backref('careers', lazy='dynamic'),
        lazy='dynamic',
    )

    def to_dict(self):
        """Serialize for JSON API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'industry': self.industry,
            'avg_salary': self.avg_salary,
            'growth_rate': self.growth_rate,
            'skills': [s.name for s in self.skills],
        }

    def __repr__(self):
        return f'<Career {self.title}>'


class Skill(db.Model):
    """A skill tag (e.g., 'Python', 'Data Analysis')."""

    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=True)  # 'technical', 'soft', etc.

    def __repr__(self):
        return f'<Skill {self.name}>'
