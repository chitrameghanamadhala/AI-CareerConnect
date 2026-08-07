"""
tests/test_services.py — Service Unit Tests
==============================================
Why this file exists:
    Tests the business logic in the services layer. Services are the
    core of the app — testing them independently of routes ensures
    the logic is correct regardless of how it's invoked.
"""

from app.utils.validators import validate_email, validate_password, validate_username
from app.utils.helpers import truncate, slugify


class TestValidators:
    """Tests for input validation functions."""

    def test_valid_email(self):
        is_valid, error = validate_email('user@example.com')
        assert is_valid is True
        assert error is None

    def test_invalid_email(self):
        is_valid, error = validate_email('not-an-email')
        assert is_valid is False
        assert 'Invalid' in error

    def test_empty_email(self):
        is_valid, error = validate_email('')
        assert is_valid is False

    def test_valid_password(self):
        is_valid, error = validate_password('secure123')
        assert is_valid is True

    def test_short_password(self):
        is_valid, error = validate_password('ab')
        assert is_valid is False

    def test_valid_username(self):
        is_valid, error = validate_username('john_doe')
        assert is_valid is True

    def test_username_special_chars(self):
        is_valid, error = validate_username('user@name!')
        assert is_valid is False


class TestHelpers:
    """Tests for helper functions."""

    def test_truncate_short_text(self):
        assert truncate('hello', 100) == 'hello'

    def test_truncate_long_text(self):
        long_text = 'a ' * 100
        result = truncate(long_text, 20)
        assert len(result) <= 25  # 20 + suffix
        assert result.endswith('...')

    def test_slugify(self):
        assert slugify('Hello World') == 'hello-world'
        assert slugify('  Spaces & Symbols!  ') == 'spaces-symbols'
