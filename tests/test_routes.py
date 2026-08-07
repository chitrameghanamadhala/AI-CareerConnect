"""
tests/test_routes.py — Route Integration Tests
=================================================
Why this file exists:
    Tests route handlers end-to-end using Flask's test client. Verifies
    that pages render, forms submit, redirects work, and protected
    routes require authentication.
"""


class TestAuthRoutes:
    """Tests for authentication routes."""

    def test_login_page_renders(self, client):
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Sign In' in response.data

    def test_register_page_renders(self, client):
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Create Account' in response.data

    def test_register_creates_user(self, client, db):
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client, sample_user):
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_with_invalid_credentials(self, client, sample_user):
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }, follow_redirects=True)
        assert b'Invalid' in response.data


class TestDashboardRoutes:
    """Tests for dashboard routes."""

    def test_dashboard_requires_login(self, client):
        response = client.get('/')
        assert response.status_code == 302  # redirect to login


class TestAPIRoutes:
    """Tests for API endpoints."""

    def test_chat_requires_login(self, client):
        response = client.post('/api/chat', json={'message': 'hello'})
        assert response.status_code == 302  # redirect to login

    def test_stt_requires_login(self, client):
        response = client.post('/api/speech-to-text')
        assert response.status_code == 302
