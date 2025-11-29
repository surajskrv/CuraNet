from flask import current_app as app, jsonify, request
from flask_security import auth_required, roles_accepted
from ..extensions import db
from ..models import User, Doctor, Patient, Department, Appointment, Treatment, DoctorAvailability
from datetime import date, datetime, timedelta
from sqlalchemy import func, or_
import re

@app.route('/api/admin/dashboard', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def admin_dashboard():
    try:
        total_doctors = Doctor.query.filter_by(is_active=True).count()
        total_patients = Patient.query.filter_by(is_active=True).count()
        total_appointments = Appointment.query.count()
        upcoming_appointments = Appointment.query.filter(
            Appointment.date >= date.today(),
            Appointment.status == 'Booked'
        ).count()
        
        return jsonify({
            'total_doctors': total_doctors,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments
        }), 200
    except Exception as e:
        return jsonify({"message": "Error fetching dashboard data", "error": str(e)}), 500

@app.route('/api/admin/doctors', methods=['GET', 'POST'])
@auth_required('token')
@roles_accepted('admin')
def manage_doctors():
    try:
        if request.method == 'GET':
            doctors = Doctor.query.join(User).filter(Doctor.is_active == True).all()
            doctors_list = []
            for doctor in doctors:
                doctors_list.append({
                    'id': doctor.id,
                    'user_id': doctor.user_id,
                    'name': doctor.user.name,
                    'email': doctor.user.email,
                    'specialization': doctor.specialization,
                    'department_id': doctor.department_id,
                    'department_name': doctor.department.name if doctor.department else None,
                    'qualification': doctor.qualification,
                    'experience': doctor.experience,
                    'bio': doctor.bio,
                    'phone': doctor.user.phone,
                    'address': doctor.user.address,
                    'pincode': doctor.user.pincode
                })
            return jsonify(doctors_list), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            name = data.get('name')
            specialization = data.get('specialization')
            department_id = data.get('department_id')
            qualification = data.get('qualification', '')
            experience = data.get('experience', '')
            bio = data.get('bio', '')
            phone = data.get('phone', '')
            address = data.get('address', '')
            pincode = data.get('pincode', '')
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({"message": "Invalid email address"}), 400
            
            if not email or not password or not name or not specialization:
                return jsonify({"message": "Email, password, name, and specialization are required"}), 400
            
            if app.security.datastore.find_user(email=email):
                return jsonify({"message": "Email already exists"}), 409
            
            from flask_security import hash_password
            user = app.security.datastore.create_user(
                email=email,
                password=hash_password(password),
                name=name,
                address=address or 'Patna',
                pincode=pincode or '123456',
                phone=phone,
                roles=['doctor']
            )
            db.session.commit()
            
            doctor = Doctor(
                user_id=user.id,
                specialization=specialization,
                department_id=department_id,
                qualification=qualification,
                experience=experience,
                bio=bio
            )
            db.session.add(doctor)
            db.session.flush()  # Get doctor.id before commit
            
            if department_id:
                dept = Department.query.get(department_id)
                if dept:
                    dept.doctors_registered = Doctor.query.filter_by(department_id=department_id, is_active=True).count()
            
            db.session.commit()
            
            return jsonify({
                "message": "Doctor created successfully",
                "doctor_id": doctor.id
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error managing doctors", "error": str(e)}), 500

@app.route('/api/admin/doctors/<int:doctor_id>', methods=['PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('admin')
def update_delete_doctor(doctor_id):
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        
        if request.method == 'PUT':
            data = request.get_json()
            user = User.query.get(doctor.user_id)
            
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
            if 'specialization' in data:
                doctor.specialization = data['specialization']
            if 'department_id' in data:
                old_dept_id = doctor.department_id
                new_dept_id = data['department_id']
                doctor.department_id = new_dept_id
                db.session.flush()
                
                if old_dept_id:
                    old_dept = Department.query.get(old_dept_id)
                    if old_dept:
                        old_dept.doctors_registered = Doctor.query.filter_by(department_id=old_dept_id, is_active=True).count()
                if new_dept_id:
                    new_dept = Department.query.get(new_dept_id)
                    if new_dept:
                        new_dept.doctors_registered = Doctor.query.filter_by(department_id=new_dept_id, is_active=True).count()
            if 'qualification' in data:
                doctor.qualification = data['qualification']
            if 'experience' in data:
                doctor.experience = data['experience']
            if 'bio' in data:
                doctor.bio = data['bio']
            
            db.session.commit()
            return jsonify({"message": "Doctor updated successfully"}), 200
        
        elif request.method == 'DELETE':
            doctor.is_active = False
            user = User.query.get(doctor.user_id)
            user.active = False
            db.session.flush()
            
            if doctor.department_id:
                dept = Department.query.get(doctor.department_id)
                if dept:
                    dept.doctors_registered = Doctor.query.filter_by(department_id=doctor.department_id, is_active=True).count()
            
            db.session.commit()
            return jsonify({"message": "Doctor removed successfully"}), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating/deleting doctor", "error": str(e)}), 500

@app.route('/api/admin/appointments', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def admin_appointments():
    try:
        status_filter = request.args.get('status')
        date_filter = request.args.get('date')
        
        query = Appointment.query
        
        if status_filter:
            query = query.filter(Appointment.status == status_filter)
        if date_filter:
            query = query.filter(Appointment.date == datetime.strptime(date_filter, '%Y-%m-%d').date())
        
        appointments = query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        
        appointments_list = []
        for apt in appointments:
            appointments_list.append({
                'id': apt.id,
                'patient_id': apt.patient_id,
                'patient_name': apt.patient.user.name,
                'patient_email': apt.patient.user.email,
                'doctor_id': apt.doctor_id,
                'doctor_name': apt.doctor.user.name,
                'doctor_specialization': apt.doctor.specialization,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'reason': apt.reason,
                'created_at': apt.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify(appointments_list), 200
    except Exception as e:
        return jsonify({"message": "Error fetching appointments", "error": str(e)}), 500

@app.route('/api/admin/search', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def admin_search():
    try:
        query_type = request.args.get('type')  # 'doctor', 'patient', 'specialization'
        search_term = request.args.get('q', '')
        
        if not search_term:
            return jsonify({"message": "Search term required"}), 400
        
        if query_type == 'doctor':
            doctors = Doctor.query.join(User).filter(
                Doctor.is_active == True,
                or_(
                    User.name.ilike(f'%{search_term}%'),
                    Doctor.specialization.ilike(f'%{search_term}%')
                )
            ).all()
            
            results = []
            for doctor in doctors:
                results.append({
                    'id': doctor.id,
                    'name': doctor.user.name,
                    'email': doctor.user.email,
                    'specialization': doctor.specialization,
                    'department': doctor.department.name if doctor.department else None,
                    'qualification': doctor.qualification,
                    'experience': doctor.experience
                })
            return jsonify(results), 200
        
        elif query_type == 'patient':
            patients = Patient.query.join(User).filter(
                Patient.is_active == True,
                or_(
                    User.name.ilike(f'%{search_term}%'),
                    User.email.ilike(f'%{search_term}%'),
                    User.phone.ilike(f'%{search_term}%')
                )
            ).all()
            
            results = []
            for patient in patients:
                results.append({
                    'id': patient.id,
                    'user_id': patient.user_id,
                    'name': patient.user.name,
                    'email': patient.user.email,
                    'phone': patient.user.phone,
                    'address': patient.user.address,
                    'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d') if patient.date_of_birth else None,
                    'gender': patient.gender,
                    'blood_group': patient.blood_group
                })
            return jsonify(results), 200
        
        elif query_type == 'specialization':
            specializations = Doctor.query.filter(
                Doctor.is_active == True,
                Doctor.specialization.ilike(f'%{search_term}%')
            ).distinct(Doctor.specialization).all()
            
            results = [{'specialization': doc.specialization} for doc in specializations]
            return jsonify(results), 200
        
        return jsonify({"message": "Invalid search type"}), 400
        
    except Exception as e:
        return jsonify({"message": "Error in search", "error": str(e)}), 500

@app.route('/api/admin/departments', methods=['GET', 'POST'])
@auth_required('token')
@roles_accepted('admin')
def manage_departments():
    try:
        if request.method == 'GET':
            departments = Department.query.all()
            dept_list = []
            for dept in departments:
                # Calculate the count dynamically based on the actual Doctor table
                doc_count = Doctor.query.filter_by(department_id=dept.id, is_active=True).count()
                
                dept_list.append({
                    'id': dept.id,
                    'name': dept.name,
                    'description': dept.description,
                    'doctors_registered': doc_count, # Use the dynamic count here
                    'created_at': dept.created_at.strftime('%Y-%m-%d')
                })
            return jsonify(dept_list), 200
        
        elif request.method == 'POST':
            data = request.get_json()
            name = data.get('name')
            description = data.get('description', '')
            
            if not name:
                return jsonify({"message": "Department name is required"}), 400
            
            if Department.query.filter_by(name=name).first():
                return jsonify({"message": "Department already exists"}), 409
            
            # We don't need to pass doctors_registered here, it defaults to 0 or is calculated on GET
            department = Department(name=name, description=description)
            db.session.add(department)
            db.session.commit()
            
            return jsonify({
                "message": "Department created successfully",
                "department_id": department.id
            }), 201
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error managing departments", "error": str(e)}), 500

@app.route('/api/admin/patients/<int:patient_id>', methods=['PUT', 'DELETE'])
@auth_required('token')
@roles_accepted('admin')
def update_delete_patient(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        user = User.query.get(patient.user_id)
        
        if request.method == 'PUT':
            data = request.get_json()
            
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
            return jsonify({"message": "Patient updated successfully"}), 200
        
        elif request.method == 'DELETE':
            patient.is_active = False
            user.active = False
            db.session.commit()
            return jsonify({"message": "Patient removed successfully"}), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating/deleting patient", "error": str(e)}), 500

@app.route('/api/admin/patients', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def get_all_patients():
    try:
        patients = Patient.query.join(User).filter(Patient.is_active == True).all()
        patients_list = []
        for patient in patients:
            patients_list.append({
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
            })
        return jsonify(patients_list), 200
    except Exception as e:
        return jsonify({"message": "Error fetching patients", "error": str(e)}), 500

@app.route('/api/admin/patient-history/<int:patient_id>', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def admin_patient_history(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        appointments = Appointment.query.filter(
            Appointment.patient_id == patient_id
        ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
        
        history = []
        for apt in appointments:
            entry = {
                'appointment_id': apt.id,
                'date': apt.date.strftime('%Y-%m-%d'),
                'time': apt.time.strftime('%H:%M'),
                'status': apt.status,
                'doctor_name': apt.doctor.user.name,
                'doctor_specialization': apt.doctor.specialization,
                'reason': apt.reason
            }
            if apt.treatment:
                entry.update({
                    'diagnosis': apt.treatment.diagnosis,
                    'prescription': apt.treatment.prescription,
                    'notes': apt.treatment.notes
                })
            history.append(entry)
        
        patient_info = {
            'id': patient.id,
            'name': patient.user.name,
            'email': patient.user.email,
            'phone': patient.user.phone,
            'address': patient.user.address,
        }
        
        return jsonify({ 'patient': patient_info, 'history': history }), 200
    except Exception as e:
        return jsonify({"message": "Error fetching patient history", "error": str(e)}), 500

@app.route('/api/admin/patients/<int:patient_id>', methods=['GET'])
@auth_required('token')
@roles_accepted('admin')
def get_single_patient(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
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
    except Exception as e:
        return jsonify({"message": "Error fetching patient", "error": str(e)}), 500