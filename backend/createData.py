from flask import current_app as app
from flask_security import hash_password
from .extensions import db
from .models import Department, Doctor, Patient, DoctorAvailability
from datetime import date, time, timedelta

with app.app_context():
    db.create_all()
    
    app.security.datastore.find_or_create_role(name='admin', description = 'admin')
    app.security.datastore.find_or_create_role(name='patient', description = 'patient')
    app.security.datastore.find_or_create_role(name='doctor', description = 'doctor')
    db.session.commit()
    
    # Create departments first
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
    
    # Get departments for use
    cardiology = Department.query.filter_by(name='Cardiology').first()
    
    # Create Admin
    if not app.security.datastore.find_user(email= 'admin@hospital.com'):
        admin_user = app.security.datastore.create_user(
            email='admin@hospital.com',
            name='Admin', 
            password=hash_password('admin123'), 
            roles=['admin'],
            active=True
        )
        db.session.commit()
    
    # Create sample patient
    if not app.security.datastore.find_user(email= 'ram@gmail.com'):
        user = app.security.datastore.create_user(
            email='ram@gmail.com',
            name='Ram Kumar', 
            password=hash_password('ram123'), 
            address="Delhi", 
            pincode="000001", 
            roles=['patient'],
            active=True
        )
        db.session.commit()
        patient = Patient(user_id=user.id, date_of_birth=date(1990, 1, 1), gender='Male', blood_group='O+')
        db.session.add(patient)
        db.session.commit()
        
    # Create sample doctor
    if not app.security.datastore.find_user(email= 'doctor@gmail.com'):
        user = app.security.datastore.create_user(
            email='doctor@gmail.com',
            name='Dr. John Smith', 
            password=hash_password('doctor123'), 
            address="Delhi", 
            pincode="000001", 
            roles=['doctor'],
            active=True
        )
        db.session.commit()
        
        doctor = Doctor(user_id=user.id, specialization='Cardiology', department_id=cardiology.id, qualification='MD, MBBS', experience='10 years', bio='Expert in cardiovascular diseases')
        db.session.add(doctor)
        db.session.commit()
        
        # Create availability for next 7 days
        for i in range(7):
            avail_date = date.today() + timedelta(days=i+1)
            if avail_date.weekday() < 5:  # Monday to Friday
                for hour in range(9, 17):  # 9 AM to 5 PM
                    availability = DoctorAvailability(
                        doctor_id=doctor.id,
                        date=avail_date,
                        start_time=time(hour, 0),
                        end_time=time(hour+1, 0),
                        is_available=True
                    )
                    db.session.add(availability)
        db.session.commit()