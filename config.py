import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-wish-you-knew"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///bakery.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    # No SERVER_NAME needed for local or cloud development
    pass


class ProductionConfig(Config):
    # No SERVER_NAME needed for production on Render or most cloud platforms
    pass


# Helper function to get the right config based on env var
def get_config(env=None):
    env = env or os.environ.get("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
