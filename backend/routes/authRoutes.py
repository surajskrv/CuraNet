from flask import current_app as app, jsonify, request
from flask_security import login_user, hash_password, verify_password, auth_required, logout_user
from  ..extensions import db
from ..models import Patient
import re
from datetime import datetime

datastore = app.security.datastore

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data"}), 400
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
        user = app.security.datastore.find_user(email=email)
        if not user:
            return jsonify({"message": "User not found"}), 404
        if not verify_password(password, user.password):
            return jsonify({"message": "Invalid credentials"}), 401
        
        login_user(user)
        user_role = user.roles[0].name
        return jsonify({
            "message": "Login successful",
            "auth_token": user.get_auth_token(),
            "user_id": user.id,
            "user_role": user_role,
        }), 200
        
    except Exception as e:
        return jsonify({"message": "Problem in Login", "error": str(e)}), 500
    
    
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), 400

        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2') #
        name = data.get('name')
        address = data.get('address')
        pincode = data.get('pincode')
        phone = data.get('phone')
        blood_group = data.get('blood_group') 
        gender = data.get('gender')
        dob_str = data.get('date_of_birth') 

        # --- Validations
        if not all([email, password, name, address, pincode, phone, blood_group, gender, dob_str]):
            return jsonify({"message": "All fields are required"}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"message": "Invalid email address"}), 400

        if password2 and password != password2:
            return jsonify({"message": "Passwords do not match"}), 400

        if len(password) < 5:
            return jsonify({"message": "Password must be at least 5 characters"}), 400
        
        if app.security.datastore.find_user(email=email):
            return jsonify({"message": "Email already registered"}), 409

        # 3. Date Conversion (String -> Python Date Object)
        try:
            # Assumes frontend sends YYYY-MM-DD
            dob_date = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format"}), 400

        # 4. Create User
        user = app.security.datastore.create_user(
            email=email,
            password=hash_password(password),
            name=name,
            address=address,
            pincode=pincode,
            phone=phone,
            roles=['patient'],
            active=True
        )
        
        # Flush sends the user to DB to generate the user.id, but doesn't commit yet
        db.session.flush() 

        # 5. Create Patient Profile
        patient = Patient(
            user_id=user.id, 
            date_of_birth=dob_date, 
            gender=gender, 
            blood_group=blood_group
        )
        
        db.session.add(patient)
        
        # 6. Single Commit for both tables
        db.session.commit()
        
        # Optional: Log them in immediately (creates session cookie)
        # login_user(user) 
        
        return jsonify({
            "message" : "Registration successful",
            "auth_token": user.get_auth_token(), # Ensure your User model supports this
            "user_role": "patient",
            "user_id": user.id
        }), 201

    except Exception as e:
        db.session.rollback() # Undo changes if error occurs
        print(f"Registration Error: {e}") # Print to server console for debugging
        return jsonify({"message": "Internal Error in registration", "error": str(e)}), 500
    
@app.route('/api/logout', methods=['POST'])
@auth_required('token')
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200