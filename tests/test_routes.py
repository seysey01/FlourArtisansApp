import unittest
from flask import url_for
from app.models import db
from MY_APP import create_app
from app.models import Product, Category


class TestRoutes(unittest.TestCase):
    """Test cases for routes functionality"""

    def setUp(self):
        self.app = create_app()
        self.app.config["SERVER_NAME"] = "localhost:5000"
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
            self.assertIn(b"\xc2\xa32.50", response.data)  # Check for the price

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


if __name__ == "__main__":
    unittest.main()
