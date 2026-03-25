# app/api/auth.py
from flask import request, jsonify
from ..models import  (Profiles, Students, Instructors, Users, UserRoles) 
from ..utils.validators import check_user_exists, check_email_exists, is_valid_email, check_user_role
from ..utils.security import hash_password
from ..api import api_bp
from ..services.user_service import create_users_bulk

# Auth Routes
@api_bp.route('/auth/register', methods=['POST'])
def register():
    '''Register new profile'''
    try:
        data: dict = request.get_json(silent=True) or {}

        if not data:
            return jsonify({'message': 'Request cannot be empty'}), 400
        
        # passed to the function services/user_service.py if data is list of objects
        if isinstance(data, list):
            return create_users_bulk(data)
        
        requires = ['role', 'first_name', 'last_name', 'birth_date', 'gender', 'email', 'password']
        for require in requires:
            if require not in data:
                return jsonify({'message': f'{require} is required'}), 400
            if not data[require] or str(data[require]).strip() == '':
                return jsonify({'message': f'{require} cannot be empty'}), 400

        if any(char.isdigit() for char in str(data['first_name'])):
                return jsonify({'message': f"{data['first_name']} is invalid first name"}), 400
        
        if any(char.isdigit() for char in str(data['middle_name'])):
                return jsonify({'message': f"{data['middle_name']} is invalid middle name"}), 400
        
        if any(char.isdigit() for char in str(data['last_name'])):
                return jsonify({'message': f"{data['last_name']} is invalid last name"}), 400
        
        if check_user_exists(str(data['first_name']).strip(), str(data['last_name']).strip()):
                return jsonify({'message': 'User already exists'}), 409 # Conflict: duplicate entry
        
        if check_email_exists(str(data['email']).strip()):
                return jsonify({'message': 'Email already taken'}), 409 # Conflict: duplicate entry
        
        is_valid, error = is_valid_email(str(data['email']).strip())
        if not is_valid:
                return jsonify({'message': f"\'{data['email']}\' {error}"}), 400


        profile = Profiles(
            first_name=str(data.get('first_name')).strip(),
            middle_name=str(data.get('middle_name')).strip(),
            last_name=str(data.get('last_name')).strip(),
            suffix=data.get('suffix'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender')
            )

        def create_account():
            profile.save()
            user = Users(
                profile_id=profile.id,
                email=str(data.get('email')).strip(),
                password=hash_password(str(data.get('password')).strip())
            )
            user.save()
            user_role = UserRoles(
                user_id=user.id,
                role_id=check_user_role(data['role'])
            )
            user_role.save()

        match data:
            case {'role' : 'student'}:
                create_account()
                new_student = Students(
                    profile_id=profile.id,  # Get the profile.id
                    year_level=data.get('year_level')
                )
                new_student.save()
                return jsonify({'message': 'Profile for student is created', 'id': profile.id}), 201
            
            case {'role' : 'instructor'}:
                create_account()   
                new_instructor = Instructors(
                    profile_id=profile.id  # Get the profile.id
                )
                new_instructor.save()
                return jsonify({'message': 'Profile for instructor is created', 'id': profile.id}), 201
            
            case _:
                return jsonify({'error': 'Double check the role'}), 500
    except Exception as e:
        return jsonify({'message': e})
