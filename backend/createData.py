from backend.extensions import db
from backend.models import User, Admin, Doctor, Patient, Department

def init_db():

    existing_admin = db.session.query(User).filter_by(email='admin@hospital.com', role='admin').first()
    
    if not existing_admin:
        admin_user = Admin()
        admin_user.email = 'admin@hospital.com'
        admin_user.role = 'admin'
        admin_user.is_active = True
        admin_user.set_password('admin123') 
        
        db.session.add(admin_user)
        db.session.flush()  # Flush to get ID and ensure admin record is created
    
    # Create default deaprtment if they don't exist
    departments = [
        {'name': 'Cardiology', 'description': 'Heart and cardiovascular system'},
        {'name': 'Oncology', 'description': 'Cancer treatment and management'},
        {'name': 'General', 'description': 'General medicine and family care'},
        {'name': 'Pediatrics', 'description': 'Children\'s health and medicine'},
        {'name': 'Orthopedics', 'description': 'Bones, joints, and muscles'},
        {'name': 'Neurology', 'description': 'Brain and nervous system'},
    ]
    
    for dep_data in departments:
        with db.session.no_autoflush:
            dep = Department.query.filter_by(name=dep_data['name']).first()
        if not dep:
            dep = Department(
                name=dep_data['name'],
                description=dep_data['description']
            )
            db.session.add(dep)
    
    db.session.commit()
    print("Database Carated or modified successfully!")

