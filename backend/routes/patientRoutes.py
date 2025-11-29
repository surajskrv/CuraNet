from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_accepted, current_user
from ..extensions import db
from ..models import User, Doctor, Patient, Department, Appointment, Treatment, DoctorAvailability
from datetime import date, datetime, timedelta

@app.route('/api/patient/dashboard', methods=['GET'])
@auth_required('token')
@roles_accepted('patient')
def patient_dashboard():
    try:
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return jsonify({"message": "Patient profile not found"}), 404
        
        # Get all departments
        departments = Department.query.all()
        dept_list = []
        for dept in departments:
            dept_list.append({
                'id': dept.id,
                'name': dept.name,
                'description': dept.description,
                'doctors_registered': dept.doctors_registered
            })
        
        # Get upcoming appointments
        upcoming = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.date >= date.today(),
            Appointment.status == 'Booked'
        ).order_by(Appointment.date.asc(), Appointment.time.asc()).all()
        
        upcoming_list = []
        for apt in upcoming:
            upcoming_list.append({
                'id': apt.id,
                'doctor_id': apt.doctor_id,
                'doctor_name': apt.doctor.user.name,
                'doctor_specialization': apt.doctor.specialization,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason
            })
        
        # Get past appointments
        past = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.date < date.today()
        ).order_by(Appointment.date.desc(), Appointment.time.desc()).limit(10).all()
        
        past_list = []
        for apt in past:
            treatment_info = None
            if apt.treatment:
                treatment_info = {
                    'diagnosis': apt.treatment.diagnosis,
                    'prescription': apt.treatment.prescription,
                    'notes': apt.treatment.notes
                }
            
            past_list.append({
                'id': apt.id,
                'doctor_id': apt.doctor_id,
                'doctor_name': apt.doctor.user.name,
                'doctor_specialization': apt.doctor.specialization,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason,
                'treatment': treatment_info
            })
        
        return jsonify({
            'departments': dept_list,
            'upcoming_appointments': upcoming_list,
            'past_appointments': past_list
        }), 200
        
    except Exception as e:
        return jsonify({"message": "Error fetching dashboard data", "error": str(e)}), 500

@app.route('/api/patient/doctors', methods=['GET'])
@auth_required('token')
@roles_accepted('patient')
def search_doctors():
    try:
        specialization = request.args.get('specialization')
        doctor_name = request.args.get('name')
        department_id = request.args.get('department_id')
        
        query = Doctor.query.join(User).filter(Doctor.is_active == True)
        
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
        if doctor_name:
            query = query.filter(User.name.ilike(f'%{doctor_name}%'))
        if department_id:
            query = query.filter(Doctor.department_id == department_id)
        
        doctors = query.all()
        
        # Get availability for next 7 days
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=6)
        
        doctors_list = []
        for doctor in doctors:
            availabilities = DoctorAvailability.query.filter(
                DoctorAvailability.doctor_id == doctor.id,
                DoctorAvailability.date >= start_date,
                DoctorAvailability.date <= end_date,
                DoctorAvailability.is_available == True
            ).order_by(DoctorAvailability.date.asc(), DoctorAvailability.start_time.asc()).all()
            
            # Group by date
            availability_dict = {}
            for avail in availabilities:
                # FIX: Check if slot is booked OR completed to prevent double booking or booking completed slots
                appointment = Appointment.query.filter(
                    Appointment.doctor_id == doctor.id,
                    Appointment.date == avail.date,
                    Appointment.time == avail.start_time,
                    Appointment.status.in_(['Booked', 'Completed']) # Updated line
                ).first()
                
                if not appointment:
                    date_str = avail.date.strftime('%Y-%m-%d')
                    if date_str not in availability_dict:
                        availability_dict[date_str] = []
                    availability_dict[date_str].append({
                        'start_time': avail.start_time.strftime('%H:%M'),
                        'end_time': avail.end_time.strftime('%H:%M')
                    })
            
            doctors_list.append({
                'id': doctor.id,
                'name': doctor.user.name,
                'email': doctor.user.email,
                'specialization': doctor.specialization,
                'department_id': doctor.department_id,
                'department_name': doctor.department.name if doctor.department else None,
                'qualification': doctor.qualification,
                'experience': doctor.experience,
                'bio': doctor.bio,
                'availability': availability_dict
            })
        
        return jsonify(doctors_list), 200
        
    except Exception as e:
        return jsonify({"message": "Error searching doctors", "error": str(e)}), 500

@app.route('/api/patient/appointments', methods=['GET', 'POST'])
@auth_required('token')
@roles_accepted('patient')
def manage_appointments():
    try:
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return jsonify({"message": "Patient profile not found"}), 404
        
        if request.method == 'GET':
            status_filter = request.args.get('status')
            query = Appointment.query.filter(Appointment.patient_id == patient.id)
            
            if status_filter:
                query = query.filter(Appointment.status == status_filter)
            else:
                query = query.order_by(Appointment.date.desc(), Appointment.time.desc())
            
            appointments = query.all()
            
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
                    'doctor_id': apt.doctor_id,
                    'doctor_name': apt.doctor.user.name,
                    'doctor_specialization': apt.doctor.specialization,
                    'doctor_email': apt.doctor.user.email,
                    'date': apt.date.strftime('%Y-%m-%d'),
                    'time': apt.time.strftime('%H:%M'),
                    'status': apt.status,
                    'reason': apt.reason,
                    'treatment': treatment_info,
                    'created_at': apt.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify(appointments_list), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            doctor_id = data.get('doctor_id')
            appointment_date = data.get('date')
            appointment_time = data.get('time')
            reason = data.get('reason', '')
            
            if not doctor_id or not appointment_date or not appointment_time:
                return jsonify({"message": "Doctor ID, date, and time are required"}), 400
            
            # Parse date and time
            apt_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            apt_time = datetime.strptime(appointment_time, '%H:%M').time()
            
            # Check if doctor exists and is active
            doctor = Doctor.query.filter_by(id=doctor_id, is_active=True).first()
            if not doctor:
                return jsonify({"message": "Doctor not found"}), 404
            
            # Check if appointment date is in the past
            if apt_date < date.today():
                return jsonify({"message": "Cannot book appointment in the past"}), 400
            
            # FIX: Check for ANY existing appointment at this slot (Booked, Cancelled, or Completed)
            existing_appointment = Appointment.query.filter(
                Appointment.doctor_id == doctor_id,
                Appointment.date == apt_date,
                Appointment.time == apt_time
            ).first()
            
            if existing_appointment:
                if existing_appointment.status == 'Booked':
                    return jsonify({"message": "Time slot already booked"}), 409
                elif existing_appointment.status == 'Completed':
                    return jsonify({"message": "This slot is already completed"}), 409
                elif existing_appointment.status == 'Cancelled':
                    # Reactivate the cancelled appointment
                    existing_appointment.status = 'Booked'
                    existing_appointment.patient_id = patient.id
                    existing_appointment.reason = reason
                    existing_appointment.updated_at = datetime.utcnow()
                    
                    db.session.commit()
                    return jsonify({
                        "message": "Appointment booked successfully",
                        "appointment_id": existing_appointment.id
                    }), 201

            # Check if doctor has availability (if no existing record was found/reused)
            availability = DoctorAvailability.query.filter(
                DoctorAvailability.doctor_id == doctor_id,
                DoctorAvailability.date == apt_date,
                DoctorAvailability.start_time == apt_time,
                DoctorAvailability.is_available == True
            ).first()
            
            if not availability:
                return jsonify({"message": "Doctor not available at this time"}), 400
            
            # Create appointment
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor_id,
                date=apt_date,
                time=apt_time,
                reason=reason,
                status='Booked'
            )
            db.session.add(appointment)
            db.session.commit()
            
            return jsonify({
                "message": "Appointment booked successfully",
                "appointment_id": appointment.id
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error managing appointments", "error": str(e)}), 500

@app.route('/api/patient/appointments/<int:appointment_id>', methods=['PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('patient')
def update_cancel_appointment(appointment_id):
    try:
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return jsonify({"message": "Patient profile not found"}), 404
        
        appointment = Appointment.query.get_or_404(appointment_id)
        
        if appointment.patient_id != patient.id:
            return jsonify({"message": "Unauthorized"}), 403
        
        if request.method == 'PUT':  # Reschedule
            data = request.get_json()
            new_date = data.get('date')
            new_time = data.get('time')
            
            if not new_date or not new_time:
                return jsonify({"message": "Date and time are required"}), 400
            
            if appointment.status != 'Booked':
                return jsonify({"message": "Can only reschedule booked appointments"}), 400
            
            # Parse new date and time
            apt_date = datetime.strptime(new_date, '%Y-%m-%d').date()
            apt_time = datetime.strptime(new_time, '%H:%M').time()
            
            # Check if new slot is available
            existing = Appointment.query.filter(
                Appointment.doctor_id == appointment.doctor_id,
                Appointment.date == apt_date,
                Appointment.time == apt_time,
                Appointment.status == 'Booked',
                Appointment.id != appointment_id
            ).first()
            
            if existing:
                return jsonify({"message": "Time slot already booked"}), 409
            
            # Update appointment
            appointment.date = apt_date
            appointment.time = apt_time
            appointment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({"message": "Appointment rescheduled successfully"}), 200
        
        elif request.method == 'DELETE':  # Cancel
            if appointment.status == 'Completed':
                return jsonify({"message": "Cannot cancel completed appointment"}), 400
            
            appointment.status = 'Cancelled'
            appointment.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({"message": "Appointment cancelled successfully"}), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating/cancelling appointment", "error": str(e)}), 500

@app.route('/api/patient/treatment-history', methods=['GET'])
@auth_required('token')
@roles_accepted('patient')
def treatment_history():
    try:
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return jsonify({"message": "Patient profile not found"}), 404
        
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient.id,
            Appointment.status == 'Completed'
        ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        
        history = []
        for apt in appointments:
            if apt.treatment:
                history.append({
                    'appointment_id': apt.id,
                    'doctor_name': apt.doctor.user.name,
                    'doctor_specialization': apt.doctor.specialization,
                    'date': apt.date.strftime('%Y-%m-%d'),
                    'time': apt.time.strftime('%H:%M'),
                    'diagnosis': apt.treatment.diagnosis,
                    'prescription': apt.treatment.prescription,
                    'notes': apt.treatment.notes,
                    'created_at': apt.treatment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return jsonify(history), 200
        
    except Exception as e:
        return jsonify({"message": "Error fetching treatment history", "error": str(e)}), 500

@app.route('/api/patient/profile', methods=['GET', 'PUT'])
@auth_required('token')
@roles_accepted('patient')
def patient_profile():
    try:
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            # Create patient profile if it doesn't exist
            patient = Patient(user_id=current_user.id)
            db.session.add(patient)
            db.session.commit()
        
        if request.method == 'GET':
            return jsonify({
                'id': patient.id,
                'user_id': patient.user_id,
                'name': patient.user.name,
                'email': patient.user.email,
                'phone': patient.user.phone,
                'address': patient.user.address,
                'pincode': patient.user.pincode,
                'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else None,
                'gender': patient.gender,
                'blood_group': patient.blood_group,
                'medical_history': patient.medical_history,
                'emergency_contact': patient.emergency_contact
            }), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            user = User.query.get(patient.user_id)
            
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                if app.security.datastore.find_user(email=data['email']) and user.email != data['email']:
                    return jsonify({"message": "Email already exists"}), 409
                user.email = data['email']
            if 'phone' in data:
                user.phone = data['phone']
            if 'address' in data:
                user.address = data['address']
            if 'pincode' in data:
                user.pincode = data['pincode']
            if 'date_of_birth' in data:
                patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data['date_of_birth'] else None
            if 'gender' in data:
                patient.gender = data['gender']
            if 'blood_group' in data:
                patient.blood_group = data['blood_group']
            if 'medical_history' in data:
                patient.medical_history = data['medical_history']
            if 'emergency_contact' in data:
                patient.emergency_contact = data['emergency_contact']
            
            db.session.commit()
            
            return jsonify({"message": "Profile updated successfully"}), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error managing profile", "error": str(e)}), 500

@app.route('/api/patient/search', methods=['GET'])
@auth_required('token')
@roles_accepted('patient')
def patient_search():
    try:
        search_type = request.args.get('type')  # 'specialization', 'doctor'
        search_term = request.args.get('q', '')
        
        if not search_term:
            return jsonify({"message": "Search term required"}), 400
        
        if search_type == 'specialization':
            specializations = Doctor.query.filter(
                Doctor.is_active == True,
                Doctor.specialization.ilike(f'%{search_term}%')
            ).distinct(Doctor.specialization).all()
            
            results = [{'specialization': doc.specialization} for doc in specializations]
            return jsonify(results), 200
        
        elif search_type == 'doctor':
            doctors = Doctor.query.join(User).filter(
                Doctor.is_active == True,
                User.name.ilike(f'%{search_term}%')
            ).all()
            
            results = []
            for doctor in doctors:
                results.append({
                    'id': doctor.id,
                    'name': doctor.user.name,
                    'specialization': doctor.specialization,
                    'department': doctor.department.name if doctor.department else None
                })
            return jsonify(results), 200
        
        return jsonify({"message": "Invalid search type"}), 400
        
    except Exception as e:
        return jsonify({"message": "Error in search", "error": str(e)}), 500