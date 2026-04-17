# app/api/auth.py

from flask import request, jsonify

from ..api import api_bp
from ..models import Profiles, Students, Instructors, Users, UserRoles
from ..services.user_service import create_users_bulk, check_require_fields
from ..utils.security import hash_password
from ..utils.validators import (
    check_user_exists,
    check_email_exists,
    is_valid_email,
    check_user_role,
)


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user profile."""
    try:
        # Get JSON request body
        data = request.get_json(silent=True) or {}

        # Check if request body is empty
        if not data:
            return jsonify({'message': 'Request cannot be empty'}), 400

        # Handle bulk registration
        if isinstance(data, list):
            result = create_users_bulk(data)

            # If something unexpected happened inside the service
            if not result.get('success'):
                return jsonify(result), 500

            # Check if at least one account was saved
            if len(result.get('saved_accounts', [])) > 0:
                return jsonify(result), 201

            # If nothing was saved, return validation errors
            return jsonify(result), 400

        # Check required fields
        if not check_require_fields(data):
            return jsonify({'message': 'Please fill all required fields'}), 400

        # Clean input values
        first_name = str(data.get('first_name', '')).strip()
        middle_name = str(data.get('middle_name', '')).strip()
        last_name = str(data.get('last_name', '')).strip()
        email = str(data.get('email', '')).strip()
        password = str(data.get('password', '')).strip()
        role = str(data.get('role', '')).strip().lower()

        # Validate first name
        if any(char.isdigit() for char in first_name):
            return jsonify({
                'message': f'{first_name} is an invalid first name'
            }), 400

        # Validate middle name only if it has a value
        if middle_name and any(char.isdigit() for char in middle_name):
            return jsonify({
                'message': f'{middle_name} is an invalid middle name'
            }), 400

        # Validate last name
        if any(char.isdigit() for char in last_name):
            return jsonify({
                'message': f'{last_name} is an invalid last name'
            }), 400

        # Check if user already exists
        if check_user_exists(first_name, last_name):
            return jsonify({
                'message': 'User already exists'
            }), 409

        # Validate email format
        is_valid, email_or_error = is_valid_email(email)

        if not is_valid:
            return jsonify({
                'message': f"'{email}' {email_or_error}"
            }), 400

        # Use normalized email from validator
        email = email_or_error

        # Check if email already exists
        if check_email_exists(email):
            return jsonify({
                'message': 'Email already taken'
            }), 409

        # Create profile record
        profile = Profiles(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            suffix=data.get('suffix'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender')
        )
        profile.save()

        # Create user record
        user = Users(
            profile_id=profile.id,
            email=email,
            password=hash_password(password)
        )
        user.save()

        # Create role mapping record
        user_role = UserRoles(
            user_id=user.id,
            role_id=check_user_role(role)
        )
        user_role.save()

        # Create student record
        if role == 'student':
            student = Students(
                profile_id=profile.id,
                year_level=data.get('year_level') or 0
            )
            student.save()

            return jsonify({
                'message': 'Student profile created successfully',
                'id': profile.id
            }), 201

        # Create instructor record
        elif role == 'instructor':
            instructor = Instructors(
                profile_id=profile.id
            )
            instructor.save()

            return jsonify({
                'message': 'Instructor profile created successfully',
                'id': profile.id
            }), 201

        # Invalid role
        return jsonify({
            'message': 'Invalid role provided'
        }), 400

    except Exception as e:
        return jsonify({
            'message': 'Something went wrong',
            'error': str(e)
        }), 500
