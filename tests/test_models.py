"""
tests/test_models.py — Model Unit Tests
==========================================
Why this file exists:
    Tests the database models in isolation — user creation, password
    hashing, career-skill relationships, conversation creation.
    Runs against an in-memory SQLite DB (via conftest.py fixtures).
"""

from app.models.user import User
from app.models.career import Career, Skill
from app.models.conversation import Conversation, Message


class TestUserModel:
    """Tests for the User model."""

    def test_create_user(self, db):
        user = User(username='john', email='john@example.com')
        user.set_password('secret')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'john'

    def test_password_hashing(self, db):
        user = User(username='jane', email='jane@example.com')
        user.set_password('mypassword')
        db.session.add(user)
        db.session.commit()

        assert user.check_password('mypassword') is True
        assert user.check_password('wrongpassword') is False
        assert user.password_hash != 'mypassword'

    def test_duplicate_email_rejected(self, db, sample_user):
        user2 = User(username='other', email=sample_user.email)
        user2.set_password('password')
        db.session.add(user2)

        import pytest
        with pytest.raises(Exception):
            db.session.commit()


class TestCareerModel:
    """Tests for the Career and Skill models."""

    def test_create_career(self, db):
        career = Career(
            title='Data Scientist',
            description='Analyze data for insights',
            industry='Technology',
            avg_salary=120000,
            growth_rate=22.0,
        )
        db.session.add(career)
        db.session.commit()

        assert career.id is not None
        assert career.title == 'Data Scientist'

    def test_career_skill_relationship(self, db):
        career = Career(title='ML Engineer', industry='Tech')
        skill = Skill(name='Python', category='technical')
        career.skills.append(skill)
        db.session.add(career)
        db.session.commit()

        assert skill in career.skills.all()
        assert career in skill.careers.all()


class TestConversationModel:
    """Tests for the Conversation and Message models."""

    def test_create_conversation(self, db, sample_user):
        conv = Conversation(user_id=sample_user.id, title='Career chat')
        db.session.add(conv)
        db.session.commit()

        assert conv.id is not None
        assert conv.user_id == sample_user.id

    def test_add_messages(self, db, sample_user):
        conv = Conversation(user_id=sample_user.id)
        db.session.add(conv)
        db.session.flush()

        msg = Message(conversation_id=conv.id, role='user', content='Hello')
        db.session.add(msg)
        db.session.commit()

        assert conv.messages.count() == 1
        assert conv.messages.first().content == 'Hello'
