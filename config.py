# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-wish-you-knew"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True