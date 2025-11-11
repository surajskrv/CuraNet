from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.models import User, Doctor, Patient, Admin, Department
from backend.extensions import db
from backend.utils import safe_cache_delete
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    role = data.get('role', 'patient')
    
    password = data.get('password', '').strip()
    email = data.get('email', '').strip()
    
    if not password:
        return jsonify({'message': 'Password is required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if email and User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    try:
        if role == 'patient':
            # Validate patient required fields before creating anything
            required_fields = ['first_name', 'last_name', 'date_of_birth', 'contact_number']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({'message': f'{field} is required for patient registration'}), 400
            
            # Create patient directly (polymorphic inheritance handles User table)
            patient = Patient()
            patient.username = username
            patient.email = email
            patient.role = 'patient'
            patient.is_active = True
            patient.set_password(password)
            patient.first_name = data['first_name']
            patient.last_name = data['last_name']
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            patient.contact_number = data['contact_number']
            patient.address = data.get('address', '')
            
            db.session.add(patient)
            db.session.commit()
            
            # Clear cache
            safe_cache_delete('admin:patients:all')
            
            return jsonify({
                'message': 'Registration successful',
                'user': patient.to_dict()
            }), 201
            
    except ValueError as e:
        db.session.rollback()
        return jsonify({'message': f'Invalid date format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/specializations', methods=['GET'])
def get_specializations():
    """Public endpoint to get all specializations (for registration)"""
    specializations = Specialization.query.all()
    return jsonify([spec.to_dict() for spec in specializations]), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    # Check cache first (safe cache handling)
    from backend.utils import safe_cache_get, safe_cache_set
    cache_key = f"user:{data['username']}"
    user_dict = safe_cache_get(cache_key)
    
    user = None
    if user_dict:
        # Try to reconstruct user from cache, but query if needed
        user = User.query.get(user_dict.get('id'))
    
    if not user:
        # Try username first, then email as fallback
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            user = User.query.filter_by(email=data['username']).first()
        if user:
            safe_cache_set(cache_key, user.to_dict(), timeout=300)
    
    if not user or not isinstance(user, User):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Check password
    if not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    # Check if user is active
    if not user.is_active:
        return jsonify({'message': 'Account is blacklisted. Please contact admin.'}), 403
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    # Get role-specific data
    user_data = None
    if user.role == 'doctor':
        doctor = Doctor.query.get(user.id)
        user_data = doctor.to_dict() if doctor else user.to_dict()
    elif user.role == 'patient':
        patient = Patient.query.get(user.id)
        user_data = patient.to_dict() if patient else user.to_dict()
    elif user.role == 'admin':
        user_data = user.to_dict()
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user_data
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged in user details"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Get role-specific data
    if user.role == 'doctor':
        doctor = Doctor.query.get(user.id)
        return jsonify(doctor.to_dict() if doctor else user.to_dict()), 200
    elif user.role == 'patient':
        patient = Patient.query.get(user.id)
        return jsonify(patient.to_dict() if patient else user.to_dict()), 200
    else:
        return jsonify(user.to_dict()), 200
