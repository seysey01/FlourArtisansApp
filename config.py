import os



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-wish-you-knew"
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://root:@localhost/bakeryApp.db"
    #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://seyamoak:passpass@localhost/bakeryApp.db"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///bakery.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True