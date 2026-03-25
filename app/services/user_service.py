# root/app/services/user_service.py

from ..models import (Profiles, Users, Students, Instructors, UserRoles)
from ..utils.security import hash_password
from flask import jsonify
from ..utils.validators import check_user_exists, check_email_exists, check_user_role, is_valid_email


# this is for the bulk requests
def create_users_bulk(data_list):
    profiles = []
    not_saved = []
    not_save_email = []
    try:
        for data in data_list:

            # Check the requires input
            requires = ['role', 'first_name', 'last_name', 'birth_date', 'gender', 'email', 'password']
            for require in requires:
                if require not in data:
                    return jsonify({'message': f'{require} is required'}), 400
                if not data[require] or str(data[require]).strip() == '':
                    return jsonify({'message': f'{require} cannot be empty'}), 400
            
            # Validate user name input
            if any(char.isdigit() for char in str(data['first_name'])):
                return jsonify({'message': f"{data['first_name']} is invalid first name"}), 400
            if any(char.isdigit() for char in str(data['middle_name'])):
                return jsonify({'message': f"{data['middle_name']} is invalid middle name"}), 400
            if any(char.isdigit() for char in str(data['last_name'])):
                return jsonify({'message': f"{data['last_name']} is invalid last name"}), 400
            
            # Check if user already exists
            if check_user_exists(str(data['first_name']).strip(), str(data['last_name']).strip()):
                not_saved.append(f"{data['first_name']} {data['last_name']}")
                continue
            # Validate emails
            is_valid, error = is_valid_email(str(data['email']).strip())
            if not is_valid:
                return jsonify({'message': f"\'{data['email']}\' {error}"}), 400
            
            # Check emails if it already exists
            if check_email_exists(str(data['email']).strip()):
                not_save_email.append(str(data['email']).strip())
                continue

            profile = Profiles(
                first_name=str(data['first_name']).strip(),
                middle_name=str(data['middle_name']).strip(),
                last_name=str(data['last_name']).strip(),
                suffix=data['suffix'],
                birth_date=data['birth_date'],
                gender=data['gender']
            )
            profile.save()
            # Make a new dictionary for return json (serialized)
            profile_data = {
                'id': profile.id,
                'first_name': profile.first_name,
                'last_name': profile.last_name
            }
            profiles.append(profile_data)

            user = Users(
                profile_id=profile.id,
                email=str(data['email']).strip(),
                password=hash_password(str(data['password']).strip())
            )
            user.save()
            user_role = UserRoles(
                user_id=user.id,
                role_id=check_user_role(data['role'])
            )
            user_role.save()

            if str(data['role']).lower() == 'student':
                student = Students(
                    profile_id=profile.id,
                    year_level=data['year_level'] if data['year_level'] else 0
                )
                student.save()
            elif str(data['role']).lower() == 'instructor':
                instructor = Instructors(
                    profile_id=profile.id
                )
                instructor.save()

        if len(profiles) > 0:
            return jsonify({'Account save': profiles}), 201
        else:
            if len(not_saved) > 0 and len(not_save_email) <= 0:
                return jsonify({'Accounts already exists': not_saved}), 409
            elif len(not_save_email) > 0 and len(not_saved) <= 0:
                return jsonify({'Emails already exists': not_save_email}), 409
            return jsonify({
                'Accounts alreay exists': not_saved,
                'Emails already exists': not_save_email}), 409
    except Exception as e:
        return jsonify({'message': str(e)}), 500