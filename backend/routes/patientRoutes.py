from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models import User, Patient, Doctor, Appointment, Treatment, Specialization, Availability
from backend.extensions import db
from backend.utils import role_required, get_current_user, safe_cache_get, safe_cache_set, safe_cache_delete
from datetime import datetime, date, time, timedelta
from sqlalchemy import and_, or_

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('patient')
def dashboard(user):
    """Patient dashboard"""
    patient = Patient.query.get(user.id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.scheduled_date >= date.today(),
        Appointment.status == 'Booked'
    ).order_by(Appointment.scheduled_date, Appointment.scheduled_time).all()
    
    # Get all deaprtment
    deaprtment = Specialization.query.all()
    
    return jsonify({
        'patient': patient.to_dict(),
        'upcoming_appointments': [appt.to_dict() for appt in upcoming_appointments],
        'deaprtment': [spec.to_dict() for spec in deaprtment]
    }), 200

@patient_bp.route('/profile', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_profile(user):
    """Get patient profile"""
    patient = Patient.query.get(user.id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    return jsonify(patient.to_dict()), 200

@patient_bp.route('/profile', methods=['PUT'])
@jwt_required()
@role_required('patient')
def update_profile(user):
    """Update patient profile"""
    patient = Patient.query.get(user.id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'username' in data:
            if User.query.filter(User.username == data['username'], User.id != user.id).first():
                return jsonify({'message': 'Username already exists'}), 400
            patient.username = data['username']
        
        if 'email' in data:
            if User.query.filter(User.email == data['email'], User.id != user.id).first():
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
        if 'date_of_birth' in data:
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'user:{patient.username}')
        safe_cache_delete(f'patient:{patient.id}:profile')
        
        return jsonify({
            'message': 'Profile updated successfully',
            'patient': patient.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update profile: {str(e)}'}), 500

@patient_bp.route('/deaprtment', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_deaprtment(user):
    """Get all deaprtment/departments"""
    cache_key = 'patient:deaprtment:all'
    deaprtment = safe_cache_get(cache_key)
    
    if not deaprtment:
        specs = Specialization.query.all()
        deaprtment = [spec.to_dict() for spec in specs]
        safe_cache_set(cache_key, deaprtment, timeout=600)  # 10 minutes
    
    return jsonify(deaprtment), 200

@patient_bp.route('/deaprtment/<int:spec_id>/doctors', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_doctors_by_specialization(user, spec_id):
    """Get doctors by specialization"""
    specialization = Specialization.query.get(spec_id)
    if not specialization:
        return jsonify({'message': 'Specialization not found'}), 404
    
    doctors = Doctor.query.filter_by(
        specialization_id=spec_id,
        is_active=True
    ).all()
    
    return jsonify([doctor.to_dict() for doctor in doctors]), 200

@patient_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_doctor_details(user, doctor_id):
    """Get doctor details and profile"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    return jsonify(doctor.to_dict()), 200

@patient_bp.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_doctor_availability(user, doctor_id):
    """Get doctor's availability for next 7 days"""
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    today = date.today()
    week_end = today + timedelta(days=7)
    
    # Get available slots that are not booked
    availabilities = Availability.query.filter(
        Availability.doctor_id == doctor_id,
        Availability.available_date >= today,
        Availability.available_date <= week_end,
        Availability.is_available == True
    ).all()
    
    # Check which slots are already booked
    booked_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.scheduled_date >= today,
        Appointment.status == 'Booked'
    ).all()
    
    booked_slots = {(appt.scheduled_date, appt.scheduled_time) for appt in booked_appointments}
    
    available_slots = []
    for avail in availabilities:
        # Check if this slot is booked
        if (avail.available_date, avail.start_time) not in booked_slots:
            available_slots.append(avail.to_dict())
    
    return jsonify(available_slots), 200

@patient_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_appointments(user):
    """Get all appointments for the patient"""
    patient = Patient.query.get(user.id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    status = request.args.get('status', '')
    upcoming = request.args.get('upcoming', '').lower() == 'true'
    past = request.args.get('past', '').lower() == 'true'
    
    query = Appointment.query.filter(Appointment.patient_id == patient.id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    if upcoming:
        query = query.filter(Appointment.scheduled_date >= date.today())
        query = query.filter(Appointment.status == 'Booked')
        query = query.order_by(Appointment.scheduled_date, Appointment.scheduled_time)
    elif past:
        query = query.filter(Appointment.status == 'Completed')
        query = query.order_by(Appointment.scheduled_date.desc())
    else:
        query = query.order_by(Appointment.scheduled_date.desc(), Appointment.scheduled_time.desc())
    
    appointments = query.all()
    
    appointments_list = []
    for appt in appointments:
        appt_data = appt.to_dict()
        if appt.treatment:
            appt_data['treatment'] = appt.treatment.to_dict()
        appointments_list.append(appt_data)
    
    return jsonify(appointments_list), 200

@patient_bp.route('/appointments', methods=['POST'])
@jwt_required()
@role_required('patient')
def book_appointment(user):
    """Book a new appointment"""
    patient = Patient.query.get(user.id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    data = request.get_json()
    
    required_fields = ['doctor_id', 'scheduled_date', 'scheduled_time']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'message': f'{field} is required'}), 400
    
    try:
        doctor_id = data['doctor_id']
        scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date()
        scheduled_time = datetime.strptime(data['scheduled_time'], '%H:%M').time()
        
        # Check if doctor exists
        doctor = Doctor.query.get(doctor_id)
        if not doctor or not doctor.is_active:
            return jsonify({'message': 'Doctor not found or inactive'}), 404
        
        # Check if slot is available
        availability = Availability.query.filter(
            Availability.doctor_id == doctor_id,
            Availability.available_date == scheduled_date,
            Availability.start_time == scheduled_time,
            Availability.is_available == True
        ).first()
        
        if not availability:
            return jsonify({'message': 'This time slot is not available'}), 400
        
        # Check if slot is already booked
        existing_appointment = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.scheduled_date == scheduled_date,
            Appointment.scheduled_time == scheduled_time,
            Appointment.status == 'Booked'
        ).first()
        
        if existing_appointment:
            return jsonify({'message': 'This time slot is already booked'}), 400
        
        # Create appointment
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            status='Booked',
            reason=data.get('reason', '')
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'patient:{patient.id}:appointments')
        safe_cache_delete(f'doctor:{doctor_id}:appointments')
        safe_cache_delete(f'patient:doctors:{doctor_id}:availability')
        
        return jsonify({
            'message': 'Appointment booked successfully',
            'appointment': appointment.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'message': f'Invalid date/time format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to book appointment: {str(e)}'}), 500

@patient_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@jwt_required()
@role_required('patient')
def cancel_appointment(user, appointment_id):
    """Cancel an appointment"""
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    if appointment.patient_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    if appointment.status != 'Booked':
        return jsonify({'message': 'Can only cancel booked appointments'}), 400
    
    try:
        appointment.status = 'Cancelled'
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'patient:{user.id}:appointments')
        safe_cache_delete(f'doctor:{appointment.doctor_id}:appointments')
        
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to cancel appointment: {str(e)}'}), 500

@patient_bp.route('/history', methods=['GET'])
@jwt_required()
@role_required('patient')
def get_history(user):
    """Get patient's complete treatment history"""
    patient = Patient.query.get(user.id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    cache_key = f'patient:{patient.id}:history'
    history = safe_cache_get(cache_key)
    
    if not history:
        # Get all completed appointments with treatments
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.status == 'Completed'
        ).order_by(Appointment.scheduled_date.desc()).all()
        
        history = []
        for appt in appointments:
            appt_data = appt.to_dict()
            if appt.treatment:
                appt_data['treatment'] = appt.treatment.to_dict()
            history.append(appt_data)
        
        safe_cache_set(cache_key, history, timeout=300)
    
    return jsonify(history), 200

@patient_bp.route('/doctors/search', methods=['GET'])
@jwt_required()
@role_required('patient')
def search_doctors(user):
    """Search doctors by name or specialization"""
    search = request.args.get('search', '')
    
    if not search:
        return jsonify({'message': 'Search query is required'}), 400
    
    cache_key = f'patient:doctors:search:{search}'
    doctors_list = safe_cache_get(cache_key)
    
    if not doctors_list:
        query = Doctor.query.filter(Doctor.is_active == True)
        
        query = query.filter(
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

