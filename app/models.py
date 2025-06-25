from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

db = SQLAlchemy()  # Initialising the SQLAlchemy instance


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship("Product", backref="category", lazy="dynamic")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f"<Product {self.name}>"


# SHOPPING
class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("carts", lazy="dynamic"))

    def __repr__(self):
        return f"<Cart {self.id}>"


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    cart = db.relationship("Cart", backref=db.backref("items", lazy="dynamic"))
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False)
    product = db.relationship(
        "Product", backref=db.backref("cart_items", lazy="dynamic")
    )
    quantity = db.Column(db.Integer, nullable=False, default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "User", backref=db.backref(
            "orders", lazy="dynamic"))
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship("OrderItem", backref="order", lazy="dynamic")

    def __repr__(self):
        return f"<Order {self.id}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False)
    product = db.relationship(
        "Product", backref=db.backref("order_items", lazy="dynamic")
    )
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"<OrderItem {self.id}>"
