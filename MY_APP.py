from flask import Flask
from flask_login import LoginManager
from app.routes import main
from config import get_config
from app.models import db, User
from flask_migrate import Migrate
import os


# Initialising Flask-Login
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder="static")

    config_class = get_config()
    app.config.from_object(config_class)
    app.register_blueprint(main)

    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    # Initialising Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "main.login"  # Specifying the login route name

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app


# Importing and registering blueprints or routes here:
app = create_app()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Creating an admin user
        if not User.query.filter_by(username="admin").first():
            admin_user = User(
                "admin", "admin@example.com", "admin_password", is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

        # Creating a customer user
        if not User.query.filter_by(username="customer").first():
            customer_user = User(
                "customer",
                "customer@example.com",
                "customer_password",
                is_admin=False,
            )
            db.session.add(customer_user)
            db.session.commit()
            print("Customer user created successfully.")
        else:
            print("Customer user already exists.")


    # This in place of app.run(debug=True) enables debug mode for development environment,
    # while ensuring it’s off in production by default
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")

