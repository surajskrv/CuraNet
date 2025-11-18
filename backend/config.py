class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///curanet.db'
    DEBUG = True
    
    # Security configuration for curanet application
    SECRET_KEY = 'hospital-secret-key-for-hashing-user-credentials' # hash user credentials in session 
    SECURITY_PASSWORD = 'bcrypt' # Mechanism for password hashing
    SECURITY_PASSWORD_SALT = 'hospital-password-salt-really-hard-to-crack' # help in password hashing
    WTF_CSRF_ENABLED = False # Disable CSRF protection for testing
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Auth-Token' # Use token authentication