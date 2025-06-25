import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-wish-you-knew"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///bakery.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    SERVER_NAME = "localhost:5000"  # For local testing


class ProductionConfig(Config):
    SERVER_NAME = None


# Helper function to get the right config based on env var
def get_config(env=None):
    env = env or os.environ.get("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
