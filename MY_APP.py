# from flask import Flask
# from app.routes import main
# from config import Config
# from app.models import db, User
# from flask_migrate import Migrate
#
#
#
# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(main)
#     app.config.from_object(Config)
#
#     db.init_app(app)  # Initialising SQLAlchemy with the Flask app instance
#
#     migrate = Migrate(app, db)
#     migrate.init_app(app, db)  # Initialising Flask-Migrate with the app and db instances
#
#
#     with app.app_context():
#         db.create_all()  # Creating the database tables
#
#     return app
#
#
# # if __name__ == "__main__" :
# #     app = create_app()
# #     app.run(debug=True)
#
# #AUTHENTICATION: username = 'admin' && password = 'admin_password'
# app = create_app()# Import and register blueprints or routes here
#
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#
#         # Creating an admin user
#         if not User.query.filter_by(username='admin').first():
#             admin_user = User('admin', 'admin_password', is_admin=True)
#             db.session.add(admin_user)
#             db.session.commit()
#             print('Admin user created successfully.')
#         else:
#             print('Admin user already exists.')
#
#     app.run(debug=True)


#-----------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------#




from flask import Flask
from flask_login import LoginManager
from app.routes import main
from config import Config
from app.models import db, User
from flask_migrate import Migrate

# Initialising Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    # Initialising Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Specifying the login route name

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app



#AUTHENTICATION: username = 'admin' && password = 'admin_password'
app = create_app()# Importing and registering blueprints or routes here

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Creating an admin user
        if not User.query.filter_by(username='admin').first():
            admin_user = User('admin', 'admin@example.com', 'admin_password', is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
            print('Admin user created successfully.')
        else:
            print('Admin user already exists.')

    app.run(debug=True)


