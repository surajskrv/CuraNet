from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'doctor', 'patient'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Polymorphic relationships
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User email :- {self.email}>'

class Admin(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
    def __repr__(self):
        return f'<Admin {self.email}>'

class Doctor(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }
    
    # Relationships
    department_rel = relationship('Department', back_populates='doctor')
    appointments = relationship('Appointment', back_populates='doctor', lazy=True, cascade='all, delete-orphan')
    availabilities = relationship('Availability', back_populates='doctor', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'department': self.department_rel.name if self.department_rel else None,
            'department_id': self.department_id,
            'experience_years': self.experience_years,
            'qualifications': self.qualifications,
            'bio': self.bio,
            'contact_number': self.contact_number,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Doctor {self.first_name} {self.last_name}>'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    doctors = relationship('Doctor', back_populates='department_rel')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def __repr__(self):
        return f'<Specialization {self.name}>'

class Patient(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }
    
    appointments = relationship('Appointment', back_populates='patient', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f'{self.first_name} {self.last_name}',
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'contact_number': self.contact_number,
            'address': self.address,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    scheduled_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='Booked')  # 'Booked', 'Completed', 'Cancelled'
    reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    patient = relationship('Patient', back_populates='appointment')
    doctor = relationship('Doctor', back_populates='appointment')
    treatment = relationship('Treatment', back_populates='appointment', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient_name': self.patient.full_name if self.patient else None,
            'doctor_name': self.doctor.full_name if self.doctor else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'scheduled_time': self.scheduled_time.strftime('%H:%M') if self.scheduled_time else None,
            'status': self.status,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'department': self.doctor.department_rel.name if self.doctor and self.doctor.department_rel else None
        }
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.patient.first_name if self.patient else "Unknown"} with Dr. {self.doctor.first_name if self.doctor else "Unknown"}>'

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False, unique=True)
    visit_type = db.Column(db.String(50), default='In-person')  # 'In-person', 'Follow-up', 'Emergency'
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=True)  # JSON string or text
    notes = db.Column(db.Text, nullable=True)
    tests_done = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    appointment = relationship('Appointment', back_populates='treatment')
    
    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'visit_type': self.visit_type,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'medicines': self.medicines,
            'notes': self.notes,
            'tests_done': self.tests_done,
            'created_date': self.created_date.isoformat() if self.created_date else None
        }
    
    def __repr__(self):
        return f'<Treatment for Appointment {self.appointment_id}>'

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    available_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relationships
    doctor = relationship('Doctor', back_populates='availabilities')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'available_date': self.available_date.isoformat() if self.available_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'is_available': self.is_available
        }
    
    def __repr__(self):
        return f'<Availability {self.id} - Dr. {self.doctor.first_name if self.doctor else "Unknown"} on {self.available_date}>'