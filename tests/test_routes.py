import unittest
from flask import url_for
from app.models import db
from MY_APP import create_app
from app.models import Product, Category


class TestRoutes(unittest.TestCase):
    """Test cases for routes functionality"""

    def setUp(self):
        self.app = create_app()
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["SERVER_NAME"] = "localhost:5000"
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_and_login(
        self, username="user", email="user@example.com", password="pass"
    ):
        client = self.app.test_client()
        client.post(
            "/register",
            data={
                "username": username,
                "email": email,
                "password": password,
                "confirm_password": password,
                "is_admin": False,
                "submit": True,
            },
            follow_redirects=True,
        )
        client.post(
            "/login",
            data={
                "username": username,
                "password": password,
                "remember_me": False,
                "submit": True,
            },
            follow_redirects=True,
        )
        return client

    def test_home_route(self):
        with self.app.test_client() as client:
            response = client.get(url_for("main.home"))
            self.assertEqual(response.status_code, 200)

    def test_yum_route(self):
        with self.app.test_client() as client:
            category = Category(name="Bakery")
            db.session.add(category)
            db.session.commit()

            product = Product(
                name="Croissant",
                description="Flaky and buttery",
                price=2.50,
                category=category,
            )
            db.session.add(product)
            db.session.commit()

            response = client.get(url_for("main.yum"))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Croissant", response.data)
            self.assertIn(b"\xc2\xa32.50", response.data)  # Checking for the price

    def test_register_route(self):
        with self.app.test_client() as client:
            response = client.post(
                "/register",
                data={
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "password": "newpass",
                    "confirm_password": "newpass",
                    "is_admin": False,
                    "submit": True,
                },
                follow_redirects=True,
            )
            self.assertIn(b"registration successful", response.data.lower())

    def test_catalog_route(self):
        with self.app.test_client() as client:
            category = Category(name="Bakery")
            db.session.add(category)
            db.session.commit()
            product = Product(
                name="Croissant",
                description="Flaky and buttery",
                price=2.50,
                category=category,
            )
            db.session.add(product)
            db.session.commit()

            response = client.get(url_for("main.catalog"))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Croissant", response.data)
            self.assertIn(b"Bakery", response.data)

    def test_login_route(self):
        with self.app.test_client() as client:
            # First register
            client.post(
                "/register",
                data={
                    "username": "loginuser",
                    "email": "loginuser@example.com",
                    "password": "loginpass",
                    "confirm_password": "loginpass",
                    "is_admin": False,
                    "submit": True,
                },
                follow_redirects=True,
            )
            # Then login
            response = client.post(
                "/login",
                data={
                    "username": "loginuser",
                    "password": "loginpass",
                    "remember_me": False,
                    "submit": True,
                },
                follow_redirects=True,
            )
            self.assertIn(b"login successful", response.data.lower())

    def test_logout_route(self):
        client = self.register_and_login(
            "logoutuser", "logoutuser@example.com", "logoutpass"
        )
        response = client.get("/logout", follow_redirects=True)
        self.assertIn(b"you have been logged out", response.data.lower())

    def test_add_to_cart_authenticated(self):
        with self.app.test_client() as client:
            # Register the user
            client.post(
                "/register",
                data={
                    "username": "testuser",
                    "email": "testuser@example.com",
                    "password": "testpass",
                    "confirm_password": "testpass",
                    "is_admin": False,
                    "submit": True,
                },
                follow_redirects=True,
            )

            # Log in the user
            client.post(
                "/login",
                data={
                    "username": "testuser",
                    "password": "testpass",
                    "remember_me": False,
                    "submit": True,
                },
                follow_redirects=True,
            )

            # Create product and category
            category = Category(name="Pastry")
            db.session.add(category)
            db.session.commit()
            product = Product(
                name="Danish", description="Sweet", price=1.5, category=category
            )
            db.session.add(product)
            db.session.commit()

            # Add to cart using the session-based endpoint
            response = client.post(
                "/add_to_cart",
                data={"item_id": str(product.id), "quantity": 1},
                follow_redirects=True,
            )

            self.assertIn(b"item added to cart", response.data.lower())

    def test_contact_route(self):
        with self.app.test_client() as client:
            response = client.get("/contact")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"contact", response.data.lower())

    def test_discounts_route(self):
        with self.app.test_client() as client:
            response = client.get("/discounts")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"watch this space", response.data.lower())

    def test_remove_from_cart_redirects_for_anonymous(self):
        with self.app.test_client() as client:
            response = client.post("/remove_from_cart/1", follow_redirects=True)
            self.assertIn(b"please log in to access your cart", response.data.lower())

    def test_cart_requires_login(self):
        with self.app.test_client() as client:
            response = client.get("/cart", follow_redirects=True)
            self.assertIn(b"please log in to access your cart", response.data.lower())


if __name__ == "__main__":
    unittest.main()
