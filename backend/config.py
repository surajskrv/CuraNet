import os

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class LocalDevelopmentConfig(Config):
    # Use the DATABASE_URL environment variable if it exists (Production), 
    # otherwise fallback to SQLite (Local)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///curanet.db')
    
    # Fix for some Postgres providers that use 'postgres://' instead of 'postgresql://'
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    DEBUG = True
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hospital-secret-key-for-hashing-user-credentials')
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'hospital-password-salt-really-hard-to-crack')
    WTF_CSRF_ENABLED = False 
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Auth-Token'