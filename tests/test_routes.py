import unittest
from flask import url_for
from app.models import db
from MY_APP import create_app
from app.models import User, Product, Category


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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
            self.assertIn(
                b"\xc2\xa32.50", response.data
            )  # Check for the price

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

    def test_new_catalog_item_route(self):
        with self.app.test_client() as client:
            # Create an admin user
            user = User(
                username="admin",
                email="admin@example.com",
                password="admin_password",
                is_admin=True,
            )
            db.session.add(user)
            db.session.commit()

            # Login as admin
            client.post(
                url_for("main.login"),
                data=dict(username="admin", password="admin_password"),
                follow_redirects=True,
            )

            # Add a new category
            category = Category(name="Bakery")
            db.session.add(category)
            db.session.commit()

            # Add a new product
            data = dict(
                name="Croissant",
                description="Flaky and buttery",
                price=2.50,
                category_id=category.id,
            )
            response = client.post(
                url_for("main.new_catalog_item"),
                data=data,
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"New product added successfully.", response.data)

    def test_login_route(self):
        with self.app.test_client() as client:
            # Create a user
            user = User(
                username="testuser",
                email="test@example.com",
                password="password",
            )
            db.session.add(user)
            db.session.commit()

            # Test login with correct credentials
            response = client.post(
                url_for("main.login"),
                data=dict(username="testuser", password="password"),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login successful!", response.data)

            # Test login with incorrect credentials
            response = client.post(
                url_for("main.login"),
                data=dict(username="testuser", password="wrongpassword"),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Invalid username or password", response.data)


if __name__ == "__main__":
    unittest.main()
