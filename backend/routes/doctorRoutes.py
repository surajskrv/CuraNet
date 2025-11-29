from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_accepted, current_user
from ..extensions import db
from ..models import User, Doctor, Patient, Appointment, Treatment, DoctorAvailability
from datetime import date, datetime, timedelta, time as dt_time
from sqlalchemy import or_

@app.route('/api/doctor/dashboard', methods=['GET'])
@auth_required('token')
@roles_accepted('doctor')
def doctor_dashboard():
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return jsonify({"message": "Doctor profile not found"}), 404
        
        today = date.today()
        week_start = today
        week_end = today + timedelta(days=7)
        
        # Today's appointments
        today_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date == today,
            Appointment.status == 'Booked'
        ).count()
        
        # Week's appointments
        week_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date >= week_start,
            Appointment.date <= week_end,
            Appointment.status == 'Booked'
        ).count()
        
        # Upcoming appointments
        upcoming = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.date >= today,
            Appointment.status == 'Booked'
        ).order_by(Appointment.date.asc(), Appointment.time.asc()).limit(10).all()
        
        upcoming_list = []
        for apt in upcoming:
            upcoming_list.append({
                'id': apt.id,
                'patient_id': apt.patient_id,
                'patient_name': apt.patient.user.name,
                'patient_email': apt.patient.user.email,
                'patient_phone': apt.patient.user.phone,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason
            })
        
        # Assigned patients
        patients_query = db.session.query(Patient).join(Appointment).filter(
            Appointment.doctor_id == doctor.id
        ).distinct().all()
        
        patients_list = []
        for patient in patients_query:
            patients_list.append({
                'id': patient.id,
                'name': patient.user.name,
                'email': patient.user.email,
                'phone': patient.user.phone,
                'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else None,
                'gender': patient.gender,
                'blood_group': patient.blood_group
            })
        
        return jsonify({
            'today_appointments': today_appointments,
            'week_appointments': week_appointments,
            'upcoming_appointments': upcoming_list,
            'assigned_patients': patients_list
        }), 200
        
    except Exception as e:
        return jsonify({"message": "Error fetching dashboard data", "error": str(e)}), 500

@app.route('/api/doctor/appointments', methods=['GET'])
@auth_required('token')
@roles_accepted('doctor')
def doctor_appointments():
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return jsonify({"message": "Doctor profile not found"}), 404
        
        status_filter = request.args.get('status')
        date_filter = request.args.get('date')
        
        query = Appointment.query.filter(Appointment.doctor_id == doctor.id)
        
        if status_filter:
            query = query.filter(Appointment.status == status_filter)
        if date_filter:
            query = query.filter(Appointment.date == datetime.strptime(date_filter, '%Y-%m-%d').date())
        else:
            query = query.filter(Appointment.date >= date.today())
        
        appointments = query.order_by(Appointment.date.asc(), Appointment.time.asc()).all()
        
        appointments_list = []
        for apt in appointments:
            treatment_info = None
            if apt.treatment:
                treatment_info = {
                    'diagnosis': apt.treatment.diagnosis,
                    'prescription': apt.treatment.prescription,
                    'notes': apt.treatment.notes
                }
            
            appointments_list.append({
                'id': apt.id,
                'patient_id': apt.patient_id,
                'patient_name': apt.patient.user.name,
                'patient_email': apt.patient.user.email,
                'patient_phone': apt.patient.user.phone,
                'date_of_birth': apt.patient.date_of_birth.strftime('%Y-%m-%d') if apt.patient.date_of_birth else None,
                'gender': apt.patient.gender,
                'blood_group': apt.patient.blood_group,
                'medical_history': apt.patient.medical_history,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason,
                'treatment': treatment_info
            })
        
        return jsonify(appointments_list), 200
        
    except Exception as e:
        return jsonify({"message": "Error fetching appointments", "error": str(e)}), 500

@app.route('/api/doctor/appointments/<int:appointment_id>', methods=['PUT'])
@auth_required('token')
@roles_accepted('doctor')
def update_appointment_status(appointment_id):
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return jsonify({"message": "Doctor profile not found"}), 404
        
        appointment = Appointment.query.get_or_404(appointment_id)
        
        if appointment.doctor_id != doctor.id:
            return jsonify({"message": "Unauthorized"}), 403
        
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['Booked', 'Completed', 'Cancelled']:
            return jsonify({"message": "Invalid status"}), 400
        
        appointment.status = new_status
        appointment.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({"message": "Appointment status updated successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating appointment", "error": str(e)}), 500

@app.route('/api/doctor/treatment', methods=['POST', 'PUT'])
@auth_required('token')
@roles_accepted('doctor')
def manage_treatment():
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return jsonify({"message": "Doctor profile not found"}), 404
        
        data = request.get_json()
        appointment_id = data.get('appointment_id')
        
        appointment = Appointment.query.get_or_404(appointment_id)
        
        if appointment.doctor_id != doctor.id:
            return jsonify({"message": "Unauthorized"}), 403
        
        if request.method == 'POST':
            if appointment.treatment:
                return jsonify({"message": "Treatment already exists. Use PUT to update."}), 400
            
            treatment = Treatment(
                appointment_id=appointment_id,
                diagnosis=data.get('diagnosis', ''),
                prescription=data.get('prescription', ''),
                notes=data.get('notes', '')
            )
            db.session.add(treatment)
            appointment.status = 'Completed'
            appointment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({"message": "Treatment record created successfully"}), 201
        
        elif request.method == 'PUT':
            if not appointment.treatment:
                return jsonify({"message": "Treatment record not found"}), 404
            
            treatment = appointment.treatment
            if 'diagnosis' in data:
                treatment.diagnosis = data['diagnosis']
            if 'prescription' in data:
                treatment.prescription = data['prescription']
            if 'notes' in data:
                treatment.notes = data['notes']
            
            treatment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({"message": "Treatment record updated successfully"}), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error managing treatment", "error": str(e)}), 500

@app.route('/api/doctor/patient-history/<int:patient_id>', methods=['GET'])
@auth_required('token')
@roles_accepted('doctor')
def patient_history(patient_id):
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return jsonify({"message": "Doctor profile not found"}), 404
        
        patient = Patient.query.get_or_404(patient_id)
        
        # Get all appointments with this doctor
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient_id,
            Appointment.doctor_id == doctor.id
        ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        
        history = []
        for apt in appointments:
            treatment_info = None
            if apt.treatment:
                treatment_info = {
                    'diagnosis': apt.treatment.diagnosis,
                    'prescription': apt.treatment.prescription,
                    'notes': apt.treatment.notes,
                    'created_at': apt.treatment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': apt.treatment.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            
            history.append({
                'appointment_id': apt.id,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason,
                'treatment': treatment_info
            })
        
        patient_info = {
            'id': patient.id,
            'name': patient.user.name,
            'email': patient.user.email,
            'phone': patient.user.phone,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else None,
            'gender': patient.gender,
            'blood_group': patient.blood_group,
            'medical_history': patient.medical_history,
            'emergency_contact': patient.emergency_contact
        }
        
        return jsonify({
            'patient': patient_info,
            'history': history
        }), 200
        
    except Exception as e:
        return jsonify({"message": "Error fetching patient history", "error": str(e)}), 500

@app.route('/api/doctor/availability', methods=['GET', 'POST'])
@auth_required('token')
@roles_accepted('doctor')
def manage_availability():
    try:
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return jsonify({"message": "Doctor profile not found"}), 404
        
        if request.method == 'GET':
            days = int(request.args.get('days', 7))
            start_date = date.today() + timedelta(days=1)
            end_date = start_date + timedelta(days=days-1)
            
            availabilities = DoctorAvailability.query.filter(
                DoctorAvailability.doctor_id == doctor.id,
                DoctorAvailability.date >= start_date,
                DoctorAvailability.date <= end_date
            ).order_by(DoctorAvailability.date.asc(), DoctorAvailability.start_time.asc()).all()
            
            availability_dict = {}
            for avail in availabilities:
                date_str = avail.date.strftime('%Y-%m-%d')
                if date_str not in availability_dict:
                    availability_dict[date_str] = []
                
                # Check if slot is Booked OR Completed
                # We use in_ to check multiple statuses
                appointment = Appointment.query.filter(
                    Appointment.doctor_id == doctor.id,
                    Appointment.date == avail.date,
                    Appointment.time == avail.start_time,
                    Appointment.status.in_(['Booked', 'Completed'])
                ).first()
                
                status = 'Available'
                if appointment:
                    status = appointment.status

                availability_dict[date_str].append({
                    'id': avail.id,
                    'start_time': avail.start_time.strftime('%H:%M'),
                    'end_time': avail.end_time.strftime('%H:%M'),
                    'is_available': avail.is_available and not appointment,
                    'is_booked': appointment is not None,
                    'status': status
                })
            
            return jsonify(availability_dict), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            availabilities = data.get('availabilities', [])
            
            # --- FIX: ROBUST DELETION ---
            # To prevent Unique Constraint violations due to timezone mismatches between client/server,
            # we widen the deletion window to cover Today + 14 days. 
            # This ensures we clear any existing slots in the target range before re-inserting.
            delete_start = date.today()
            delete_end = delete_start + timedelta(days=14)
            
            DoctorAvailability.query.filter(
                DoctorAvailability.doctor_id == doctor.id,
                DoctorAvailability.date >= delete_start,
                DoctorAvailability.date <= delete_end
            ).delete(synchronize_session=False)
            
            # Add new availabilities
            for avail_data in availabilities:
                try:
                    avail_date = datetime.strptime(avail_data['date'], '%Y-%m-%d').date()
                    start_time = datetime.strptime(avail_data['start_time'], '%H:%M').time()
                    end_time = datetime.strptime(avail_data['end_time'], '%H:%M').time()
                    
                    availability = DoctorAvailability(
                        doctor_id=doctor.id,
                        date=avail_date,
                        start_time=start_time,
                        end_time=end_time,
                        is_available=True 
                    )
                    db.session.add(availability)
                except ValueError:
                    continue # Skip malformed dates
            
            db.session.commit()
            
            return jsonify({"message": "Availability updated successfully"}), 200
            
    except Exception as e:
        db.session.rollback()
        # Log the specific error to help with debugging if it persists
        print(f"Error in manage_availability: {str(e)}") 
        return jsonify({"message": "Error managing availability", "error": str(e)}), 500