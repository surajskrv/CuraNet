from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models import User, Doctor, Patient, Admin, Appointment, Specialization
from backend.extensions import db
from backend.utils import role_required, get_current_user, clear_cache_pattern, safe_cache_get, safe_cache_set, safe_cache_delete
from datetime import datetime, date
from sqlalchemy import or_

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def dashboard(user):
    """Admin dashboard statistics"""
    
    # Try cache first
    cache_key = 'admin:dashboard:stats'
    stats = safe_cache_get(cache_key)
    
    if not stats:
        total_doctors = Doctor.query.count()
        total_patients = Patient.query.count()
        total_appointments = Appointment.query.count()
        upcoming_appointments = Appointment.query.filter(
            Appointment.scheduled_date >= date.today(),
            Appointment.status == 'Booked'
        ).count()
        
        stats = {
            'total_doctors': total_doctors,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments
        }
        
        safe_cache_set(cache_key, stats, timeout=300)  # 5 minutes
    
    return jsonify(stats), 200

@admin_bp.route('/doctors', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_doctors(user):
    """Get all doctors with optional search"""
    search = request.args.get('search', '')
    
    cache_key = f'admin:doctors:list:{search}'
    doctors_list = safe_cache_get(cache_key)
    
    if not doctors_list:
        query = Doctor.query
        
        if search:
            query = query.join(User).filter(
                or_(
                    Doctor.first_name.ilike(f'%{search}%'),
                    Doctor.last_name.ilike(f'%{search}%'),
                    User.username.ilike(f'%{search}%'),
                    Doctor.specialization_rel.has(Specialization.name.ilike(f'%{search}%'))
                )
            )
        
        doctors = query.all()
        doctors_list = [doctor.to_dict() for doctor in doctors]
        safe_cache_set(cache_key, doctors_list, timeout=300)
    
    return jsonify(doctors_list), 200

@admin_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_doctor(user, doctor_id):
    """Get doctor by ID"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    return jsonify(doctor.to_dict()), 200

@admin_bp.route('/doctors', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_doctor(user):
    """Create a new doctor"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'specialization_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'message': f'{field} is required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    try:
        # Create doctor user
        doctor_user = User(
            username=data['username'],
            email=data['email'],
            role='doctor',
            is_active=True
        )
        doctor_user.set_password(data['password'])
        db.session.add(doctor_user)
        db.session.flush()
        
        # Create doctor record
        doctor = Doctor(
            id=doctor_user.id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            specialization_id=data['specialization_id'],
            experience_years=data.get('experience_years'),
            qualifications=data.get('qualifications'),
            bio=data.get('bio'),
            contact_number=data.get('contact_number')
        )
        db.session.add(doctor)
        db.session.commit()
        
        # Clear cache
        clear_cache_pattern('admin:doctors:*')
        safe_cache_delete('admin:dashboard:stats')
        
        return jsonify({
            'message': 'Doctor created successfully',
            'doctor': doctor.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create doctor: {str(e)}'}), 500

@admin_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_doctor(user, doctor_id):
    """Update doctor information"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update user fields
        if 'username' in data:
            if User.query.filter(User.username == data['username'], User.id != doctor_id).first():
                return jsonify({'message': 'Username already exists'}), 400
            doctor.username = data['username']
        
        if 'email' in data:
            if User.query.filter(User.email == data['email'], User.id != doctor_id).first():
                return jsonify({'message': 'Email already exists'}), 400
            doctor.email = data['email']
        
        # Update doctor fields
        if 'first_name' in data:
            doctor.first_name = data['first_name']
        if 'last_name' in data:
            doctor.last_name = data['last_name']
        if 'specialization_id' in data:
            doctor.specialization_id = data['specialization_id']
        if 'experience_years' in data:
            doctor.experience_years = data['experience_years']
        if 'qualifications' in data:
            doctor.qualifications = data['qualifications']
        if 'bio' in data:
            doctor.bio = data['bio']
        if 'contact_number' in data:
            doctor.contact_number = data['contact_number']
        
        db.session.commit()
        
        # Clear cache
        clear_cache_pattern('admin:doctors:*')
        safe_cache_delete(f'user:{doctor.username}')
        
        return jsonify({
            'message': 'Doctor updated successfully',
            'doctor': doctor.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update doctor: {str(e)}'}), 500

@admin_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_doctor(user, doctor_id):
    """Delete/Blacklist a doctor"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    try:
        # Soft delete (blacklist)
        doctor.is_active = False
        db.session.commit()
        
        # Clear cache
        clear_cache_pattern('admin:doctors:*')
        safe_cache_delete('admin:dashboard:stats')
        safe_cache_delete(f'user:{doctor.username}')
        
        return jsonify({'message': 'Doctor blacklisted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to blacklist doctor: {str(e)}'}), 500

@admin_bp.route('/patients', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_patients(user):
    """Get all patients with optional search"""
    search = request.args.get('search', '')
    
    cache_key = f'admin:patients:list:{search}'
    patients_list = safe_cache_get(cache_key)
    
    if not patients_list:
        query = Patient.query
        
        if search:
            query = query.join(User).filter(
                or_(
                    Patient.first_name.ilike(f'%{search}%'),
                    Patient.last_name.ilike(f'%{search}%'),
                    User.username.ilike(f'%{search}%'),
                    Patient.contact_number.ilike(f'%{search}%')
                )
            )
        
        patients = query.all()
        patients_list = [patient.to_dict() for patient in patients]
        safe_cache_set(cache_key, patients_list, timeout=300)
    
    return jsonify(patients_list), 200

@admin_bp.route('/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_patient(user, patient_id):
    """Get patient by ID"""
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    return jsonify(patient.to_dict()), 200

@admin_bp.route('/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_patient(user, patient_id):
    """Update patient information"""
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'username' in data:
            if User.query.filter(User.username == data['username'], User.id != patient_id).first():
                return jsonify({'message': 'Username already exists'}), 400
            patient.username = data['username']
        
        if 'email' in data:
            if User.query.filter(User.email == data['email'], User.id != patient_id).first():
                return jsonify({'message': 'Email already exists'}), 400
            patient.email = data['email']
        
        if 'first_name' in data:
            patient.first_name = data['first_name']
        if 'last_name' in data:
            patient.last_name = data['last_name']
        if 'contact_number' in data:
            patient.contact_number = data['contact_number']
        if 'address' in data:
            patient.address = data['address']
        
        db.session.commit()
        
        # Clear cache
        clear_cache_pattern('admin:patients:*')
        safe_cache_delete(f'user:{patient.username}')
        
        return jsonify({
            'message': 'Patient updated successfully',
            'patient': patient.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update patient: {str(e)}'}), 500

@admin_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_patient(user, patient_id):
    """Blacklist a patient"""
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    try:
        patient.is_active = False
        db.session.commit()
        
        # Clear cache
        clear_cache_pattern('admin:patients:*')
        safe_cache_delete('admin:dashboard:stats')
        safe_cache_delete(f'user:{patient.username}')
        
        return jsonify({'message': 'Patient blacklisted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to blacklist patient: {str(e)}'}), 500

@admin_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_appointments(user):
    """Get all appointments"""
    status = request.args.get('status', '')
    upcoming = request.args.get('upcoming', '').lower() == 'true'
    
    cache_key = f'admin:appointments:{status}:{upcoming}'
    appointments_list = safe_cache_get(cache_key)
    
    if not appointments_list:
        query = Appointment.query
        
        if status:
            query = query.filter(Appointment.status == status)
        
        if upcoming:
            query = query.filter(Appointment.scheduled_date >= date.today())
            query = query.order_by(Appointment.scheduled_date, Appointment.scheduled_time)
        
        appointments = query.order_by(Appointment.created_at.desc()).all()
        appointments_list = [appt.to_dict() for appt in appointments]
        safe_cache_set(cache_key, appointments_list, timeout=300)
    
    return jsonify(appointments_list), 200

@admin_bp.route('/appointments/<int:appointment_id>/history', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_patient_history(user, appointment_id):
    """Get patient history for an appointment"""
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    # Get all appointments for this patient with this doctor
    patient_id = appointment.patient_id
    doctor_id = appointment.doctor_id
    
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor_id,
        status='Completed'
    ).order_by(Appointment.scheduled_date.desc()).all()
    
    history = []
    for appt in appointments:
        appt_data = appt.to_dict()
        if appt.treatment:
            appt_data['treatment'] = appt.treatment.to_dict()
        history.append(appt_data)
    
    return jsonify(history), 200

@admin_bp.route('/deaprtment', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_deaprtment(user):
    """Get all deaprtment"""
    deaprtment = Specialization.query.all()
    return jsonify([spec.to_dict() for spec in deaprtment]), 200

