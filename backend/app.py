from flask import Flask
from flask_cors import CORS
from backend.config import LocalDevelopmentConfig
from backend.extensions import db, jwt, mail, cache

app = None
celery = None

def create_app():
    global app, celery
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    # Initialize cache with error handling
    try:
        # Try Redis first if configured
        if app.config.get('REDIS_AVAILABLE', False):
            cache.init_app(app)
        else:
            # Use SimpleCache fallback
            app.config['CACHE_TYPE'] = 'SimpleCache'
            cache.init_app(app)
    except Exception as e:
        print(f"Warning: Cache initialization failed: {e}. Continuing without cache.")
        # Set SimpleCache as fallback
        app.config['CACHE_TYPE'] = 'SimpleCache'
        try:
            cache.init_app(app)
        except:
            pass  # Cache is optional
    
    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    
    # Initialize Celery (disabled for now - focus on core functionality)
    # Background jobs will be enabled later
    celery = None

    with app.app_context():
        db.create_all()
    
    from backend.routes.authRoutes import auth_bp
    from backend.routes.adminRoutes import admin_bp
    from backend.routes.doctorRoutes import doctor_bp
    from backend.routes.patientRoutes import patient_bp
    from backend.routes.taskRoutes import task_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    
    # Initialize database with admin user
    from backend.createData import init_db
    with app.app_context():
        init_db()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)