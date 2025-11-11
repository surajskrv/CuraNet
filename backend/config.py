import os

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hospitalV2-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    
    # Redis configuration - fallback to SimpleCache if Redis unavailable
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/1'
    # Default to SimpleCache, will try Redis in app initialization
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Try Redis if available (will be checked in app initialization)
    REDIS_AVAILABLE = False
    try:
        import redis
        r = redis.Redis.from_url(REDIS_URL, socket_connect_timeout=1)
        r.ping()
        REDIS_AVAILABLE = True
        CACHE_TYPE = 'RedisCache'
        CACHE_REDIS_URL = REDIS_URL
    except:
        pass  # Use SimpleCache fallback
    
    # Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@hospital.com'
    
    # Google Chat Webhook (for daily reminders)
    GOOGLE_CHAT_WEBHOOK_URL = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL') or ''
    
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    DEBUG = True
    WTF_CSRF_ENABLED = False  # Disable CSRF protection for testing