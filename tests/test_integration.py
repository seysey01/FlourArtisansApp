import unittest
from app.models import db, User, Product, Category
from MY_APP import create_app  # Replace with your actual app factory import
import os

class IntegrationTests(unittest.TestCase):
    """Comprehensive integration tests for FlourArtisansApp"""

    TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "default-test-password")

    def setUp(self):
        self.app = create_app()
        self.app.config["SERVER_NAME"] = "localhost:5000"
        self.app.config["WTF_CSRF_ENABLED"] = False  # Disabling CSRF for test POSTs
        self.app.config["PROPAGATE_EXCEPTIONS"] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page_accessible(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"home", response.data.lower())

    def test_registration_and_login(self):
        # Register a new user
        response = self.client.post("/register", data={
            "username": "integrationuser",
            "email": "integration@example.com",
            "password": self.TEST_PASSWORD,
            "confirm_password": self.TEST_PASSWORD,
            "is_admin": False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"register", response.data.lower())

        # Attempt login
        response = self.client.post("/login", data={
            "username": "integrationuser",
            "password": self.TEST_PASSWORD
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"home", response.data.lower())

    def test_catalog_route_lists_products(self):
        # Setup: create category and product
        category = Category(name="Cakes")
        db.session.add(category)
        db.session.commit()
        product = Product(
            name="Test Cake",
            description="Yummy cake",
            price=10.99,
            category=category
        )
        db.session.add(product)
        db.session.commit()
        response = self.client.get("/catalog")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Cake", response.data)
        self.assertIn(b"Cakes", response.data)

    def test_add_to_cart_requires_login(self):
        # POST to add_to_cart should redirect to login if not logged in
        response = self.client.post("/add_to_cart", data={
            "item_id": "1",
            "quantity": 1
        }, follow_redirects=True)
        self.assertIn(b"login", response.data.lower())

    def test_add_to_cart_logged_in(self):
        with self.client as c:
            # Register
            c.post("/register", data={
                "username": "cartuser",
                "email": "cart@example.com",
                "password": self.TEST_PASSWORD,
                "confirm_password": self.TEST_PASSWORD,
                "is_admin": False
            }, follow_redirects=True)
            # Login
            c.post("/login", data={
                "username": "cartuser",
                "password": self.TEST_PASSWORD
            }, follow_redirects=True)
            # Setup product with unique category
            category = Category(name="Bakery_cartuser")
            db.session.add(category)
            db.session.commit()
            product = Product(
                name="Croissant",
                description="Flaky and buttery",
                price=2.50,
                category=category
            )
            db.session.add(product)
            db.session.commit()
            # Add to cart
            response = c.post("/add_to_cart", data={
                "item_id": str(product.id),
                "quantity": 2
            }, follow_redirects=True)
            print(response.data)  # Debug: see exact output
            self.assertIn(b"item added to cart", response.data.lower())

if __name__ == "__main__":
    unittest.main()