import os

# Use local url for local testing and os var for deployment PLZ
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    #SQLALCHEMY_DATABASE_URI = "postgresql:///f1db"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
