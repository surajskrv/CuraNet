from .extensions import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String, nullable = False)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)
    
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique= True, nullable = False)
    name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable=False, default ="Patna")
    pincode = db.Column(db.String(6), nullable = False, default = '123456')
    phone = db.Column(db.String(10), nullable=False, default="0000000000")
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, nullable = False, default=True)
    roles = db.relationship('Role', backref = 'bearer', secondary= 'user_roles')
    
    # Relationships
    doctor_profile = db.relationship('Doctor', backref='user', uselist=False, cascade='all, delete-orphan')
    patient_profile = db.relationship('Patient', backref='user', uselist=False, cascade='all, delete-orphan')

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.Text, nullable = False)
    doctors_registered = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    doctors = db.relationship('Doctor', backref='department', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, unique = True)
    specialization = db.Column(db.String, nullable = False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable = True)
    qualification = db.Column(db.String, nullable = False)
    experience = db.Column(db.String, nullable = False)
    bio = db.Column(db.Text, nullable = False)
    is_active = db.Column(db.Boolean, default=True, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    availabilities = db.relationship('DoctorAvailability', backref='doctor', lazy=True, cascade='all, delete-orphan')

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False, unique = True)
    date_of_birth = db.Column(db.Date, nullable = False)
    gender = db.Column(db.String(10), nullable = False)
    blood_group = db.Column(db.String(5), nullable = False)
    medical_history = db.Column(db.Text, nullable = True)
    emergency_contact = db.Column(db.String(15), nullable = True)
    is_active = db.Column(db.Boolean, default=True, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.Time, nullable = False)
    end_time = db.Column(db.Time, nullable = False)
    is_available = db.Column(db.Boolean, default=True, nullable = False)
    
    __table_args__ = (db.UniqueConstraint('doctor_id', 'date', 'start_time', name='unique_doctor_slot'),)

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable = False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)
    status = db.Column(db.String(20), default='Booked', nullable = False)  # Booked, Completed, Cancelled
    reason = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    treatment = db.relationship('Treatment', backref='appointment', uselist=False, cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('doctor_id', 'date', 'time', name='unique_doctor_appointment'),)

class Treatment(db.Model):
    __tablename__ = 'treatment'
    id = db.Column(db.Integer, primary_key = True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable = False, unique = True)
    diagnosis = db.Column(db.Text, nullable = True)
    prescription = db.Column(db.Text, nullable = True)
    notes = db.Column(db.Text, nullable = True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    