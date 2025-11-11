from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.models import Doctor, Appointment, Treatment, Availability, Patient
from backend.extensions import db
from backend.utils import role_required, get_current_user, safe_cache_get, safe_cache_set, safe_cache_delete, clear_cache_pattern
from datetime import datetime, date, time, timedelta
from sqlalchemy import and_

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('doctor')
def dashboard(user):
    """Doctor dashboard with upcoming appointments"""
    doctor = Doctor.query.get(user.id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    # Get today's appointments
    today = date.today()
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.scheduled_date == today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.scheduled_time).all()
    
    # Get week's appointments
    week_start = today
    week_end = today + timedelta(days=7)
    week_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.scheduled_date >= week_start,
        Appointment.scheduled_date <= week_end,
        Appointment.status == 'Booked'
    ).order_by(Appointment.scheduled_date, Appointment.scheduled_time).all()
    
    # Get assigned patients count
    assigned_patients = db.session.query(Patient).join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().count()
    
    return jsonify({
        'doctor': doctor.to_dict(),
        'today_appointments': [appt.to_dict() for appt in today_appointments],
        'week_appointments': [appt.to_dict() for appt in week_appointments],
        'assigned_patients_count': assigned_patients
    }), 200

@doctor_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required('doctor')
def get_appointments(user):
    """Get all appointments for the doctor"""
    doctor = Doctor.query.get(user.id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    status = request.args.get('status', '')
    upcoming = request.args.get('upcoming', '').lower() == 'true'
    
    query = Appointment.query.filter(Appointment.doctor_id == doctor.id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    if upcoming:
        query = query.filter(Appointment.scheduled_date >= date.today())
        query = query.filter(Appointment.status == 'Booked')
    
    appointments = query.order_by(Appointment.scheduled_date, Appointment.scheduled_time).all()
    
    return jsonify([appt.to_dict() for appt in appointments]), 200

@doctor_bp.route('/patients', methods=['GET'])
@jwt_required()
@role_required('doctor')
def get_assigned_patients(user):
    """Get list of patients assigned to the doctor"""
    doctor = Doctor.query.get(user.id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    # Get unique patients who have appointments with this doctor
    patients = db.session.query(Patient).join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().all()
    
    return jsonify([patient.to_dict() for patient in patients]), 200

@doctor_bp.route('/appointments/<int:appointment_id>/complete', methods=['POST'])
@jwt_required()
@role_required('doctor')
def complete_appointment(user, appointment_id):
    """Mark appointment as completed and add treatment"""
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    if appointment.doctor_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    required_fields = ['diagnosis']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'message': f'{field} is required'}), 400
    
    try:
        # Update appointment status
        appointment.status = 'Completed'
        
        # Create or update treatment
        treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
        if not treatment:
            treatment = Treatment(appointment_id=appointment_id)
            db.session.add(treatment)
        
        treatment.visit_type = data.get('visit_type', 'In-person')
        treatment.diagnosis = data['diagnosis']
        treatment.prescription = data.get('prescription', '')
        treatment.medicines = data.get('medicines', '')
        treatment.tests_done = data.get('tests_done', '')
        treatment.notes = data.get('notes', '')
        
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'doctor:{user.id}:appointments')
        safe_cache_delete(f'patient:{appointment.patient_id}:history')
        
        return jsonify({
            'message': 'Appointment marked as completed',
            'appointment': appointment.to_dict(),
            'treatment': treatment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to complete appointment: {str(e)}'}), 500

@doctor_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@jwt_required()
@role_required('doctor')
def cancel_appointment(user, appointment_id):
    """Cancel an appointment"""
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    if appointment.doctor_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    try:
        appointment.status = 'Cancelled'
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'doctor:{user.id}:appointments')
        safe_cache_delete(f'patient:{appointment.patient_id}:appointments')
        
        return jsonify({'message': 'Appointment cancelled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to cancel appointment: {str(e)}'}), 500

@doctor_bp.route('/patients/<int:patient_id>/history', methods=['GET'])
@jwt_required()
@role_required('doctor')
def get_patient_history(user, patient_id):
    """Get full history of a patient with this doctor"""
    doctor = Doctor.query.get(user.id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({'message': 'Patient not found'}), 404
    
    # Get all completed appointments
    appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.patient_id == patient_id,
        Appointment.status == 'Completed'
    ).order_by(Appointment.scheduled_date.desc()).all()
    
    history = []
    for appt in appointments:
        appt_data = appt.to_dict()
        if appt.treatment:
            appt_data['treatment'] = appt.treatment.to_dict()
        history.append(appt_data)
    
    return jsonify(history), 200

@doctor_bp.route('/appointments/<int:appointment_id>/history', methods=['PUT'])
@jwt_required()
@role_required('doctor')
def update_patient_history(user, appointment_id):
    """Update patient history for a completed appointment"""
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404
    
    if appointment.doctor_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    if appointment.status != 'Completed':
        return jsonify({'message': 'Can only update history for completed appointments'}), 400
    
    treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
    if not treatment:
        return jsonify({'message': 'Treatment not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'visit_type' in data:
            treatment.visit_type = data['visit_type']
        if 'diagnosis' in data:
            treatment.diagnosis = data['diagnosis']
        if 'prescription' in data:
            treatment.prescription = data['prescription']
        if 'medicines' in data:
            treatment.medicines = data['medicines']
        if 'tests_done' in data:
            treatment.tests_done = data['tests_done']
        if 'notes' in data:
            treatment.notes = data['notes']
        
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'patient:{appointment.patient_id}:history')
        
        return jsonify({
            'message': 'History updated successfully',
            'treatment': treatment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update history: {str(e)}'}), 500

@doctor_bp.route('/availability', methods=['GET'])
@jwt_required()
@role_required('doctor')
def get_availability(user):
    """Get doctor's availability"""
    doctor = Doctor.query.get(user.id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Availability.query.filter(Availability.doctor_id == doctor.id)
    
    if start_date:
        query = query.filter(Availability.available_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(Availability.available_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    availabilities = query.order_by(Availability.available_date, Availability.start_time).all()
    
    return jsonify([avail.to_dict() for avail in availabilities]), 200

@doctor_bp.route('/availability', methods=['POST'])
@jwt_required()
@role_required('doctor')
def set_availability(user):
    """Set doctor availability for next 7 days"""
    doctor = Doctor.query.get(user.id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404
    
    data = request.get_json()
    
    if 'slots' not in data or not isinstance(data['slots'], list):
        return jsonify({'message': 'slots array is required'}), 400
    
    try:
        # Delete existing availability for next 7 days
        today = date.today()
        week_end = today + timedelta(days=7)
        
        Availability.query.filter(
            Availability.doctor_id == doctor.id,
            Availability.available_date >= today,
            Availability.available_date <= week_end
        ).delete()
        
        # Create new availability slots
        for slot in data['slots']:
            if not all(k in slot for k in ['date', 'start_time', 'end_time']):
                continue
            
            avail_date = datetime.strptime(slot['date'], '%Y-%m-%d').date()
            start_time_obj = datetime.strptime(slot['start_time'], '%H:%M').time()
            end_time_obj = datetime.strptime(slot['end_time'], '%H:%M').time()
            
            # Only allow setting availability for next 7 days
            if avail_date < today or avail_date > week_end:
                continue
            
            availability = Availability(
                doctor_id=doctor.id,
                available_date=avail_date,
                start_time=start_time_obj,
                end_time=end_time_obj,
                is_available=True
            )
            db.session.add(availability)
        
        db.session.commit()
        
        # Clear cache
        safe_cache_delete(f'doctor:{doctor.id}:availability')
        safe_cache_delete('patient:doctors:available:*')
        
        return jsonify({'message': 'Availability updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to set availability: {str(e)}'}), 500

