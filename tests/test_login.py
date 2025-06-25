import unittest
from app.models import db, User
from MY_APP import create_app


class TestLoginRoute(unittest.TestCase):
    """Test cases for login functionality"""

    TEST_PASSWORD = "[PASSWORD]!"  # Class constant for test password

    def setUp(self):
        """Setting up test environment before each test"""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Created test user
        self.test_user = User(
            username="testuser", email="test@example.com", password=self.TEST_PASSWORD
        )
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """Cleaning up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page_loads(self):
        """Testing that login page loads correctly"""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)
        self.assertIn(b"Remember Me", response.data)

    def test_form_validation(self):
        """Testing login form validation"""
        # Test empty submission
        response = self.client.post("/login", data={}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required", response.data)

        # Test missing password
        response = self.client.post(
            "/login", data={"username": "testuser"}, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required", response.data)

        # Test missing username
        response = self.client.post(
            "/login", data={"password": self.TEST_PASSWORD}, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required", response.data)

    def test_csrf_protection(self):
        """Testing CSRF protection"""
        with self.client as c:
            response = c.get("/login")
            self.assertIn(b"csrf_token", response.data)


if __name__ == "__main__":
    unittest.main()
