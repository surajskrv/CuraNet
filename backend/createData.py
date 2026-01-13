from flask import current_app as app
from flask_security import hash_password
from .extensions import db
from .models import Department


with app.app_context():
    db.create_all()
    
    app.security.datastore.find_or_create_role(name='admin', description = 'admin')
    app.security.datastore.find_or_create_role(name='patient', description = 'patient')
    app.security.datastore.find_or_create_role(name='doctor', description = 'doctor')
    db.session.commit()
    
    # Create departments if not exist
    if not Department.query.filter_by(name='Cardiology').first():
        cardiology = Department(name='Cardiology', description='Heart and cardiovascular diseases')
        db.session.add(cardiology)
    if not Department.query.filter_by(name='Neurology').first():
        neurology = Department(name='Neurology', description='Nervous system disorders')
        db.session.add(neurology)
    if not Department.query.filter_by(name='Orthopedics').first():
        orthopedics = Department(name='Orthopedics', description='Bone and joint diseases')
        db.session.add(orthopedics)
    if not Department.query.filter_by(name='Pediatrics').first():
        pediatrics = Department(name='Pediatrics', description='Child healthcare')
        db.session.add(pediatrics)
    db.session.commit()
    
    # Create Admin if not exist
    if not app.security.datastore.find_user(email= 'admin@gmail.com'):
        admin_user = app.security.datastore.create_user(
            email='admin@gmail.com',
            name='Admin', 
            password=hash_password('helloadmin'), 
            roles=['admin'],
            active=True
        )
        db.session.commit()
    
    