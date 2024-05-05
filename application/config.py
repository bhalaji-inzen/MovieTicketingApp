class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite3"
    DEBUG = True
    SECRET_KEY =  "random secret key"
    SECURITY_PASSWORD_HASH = "bcrypt"    
    SECURITY_PASSWORD_SALT = "for additional randomization of the password if two password of different users are same"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER='Authentication-Token'
    SECURITY_LOGIN_USER_TEMPLATE='login.html'
    SECURITY_USERNAME_ENABLE=True
    SECURITY_POST_LOGOUT_VIEW='/login'
    SECURITY_POST_REGISTER_VIEW='/login'
    CELERY_BROKER_URL='redis://localhost:6379/1'
    CELERY_RESULT_BACKEND='redis://localhost:6379/2'
    SMTP_SERVER_HOST='localhost'
    SMTP_SERVER_PORT='1025'
    SENDER_ADDRESS='admin@admin.com'
    SENDER_PASSWORD='1234'
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 60
