# from flask import Flask
#
# def create_app():
#     app = Flask(__name__)
#     return app
#
# app = create_app()
#-----------------------------------------------
# from flask import Flask
# from app.route import main
# from config import Config
#
#
#
# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(main)
#     app.config.from_object(Config)
#
#     return app