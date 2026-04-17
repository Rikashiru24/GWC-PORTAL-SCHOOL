# root/app/services/user_service.py
from ..models import Profiles, Users, Students, Instructors, UserRoles
from ..utils.security import hash_password
from ..utils.validators import (
    check_user_exists,
    check_email_exists,
    check_user_role,
    is_valid_email,
)


# List of fields required for every user
REQUIRED_FIELDS = [
    'role',
    'first_name',
    'last_name',
    'birth_date',
    'gender',
    'email',
    'password',
]


# Check if all required fields are present and not empty
def check_require_fields(data):
    for field in REQUIRED_FIELDS:
        # Check if the field does not exist
        if field not in data:
            return False

        # Check if the field exists but is empty
        if not data[field] or str(data[field]).strip() == '':
            return False

    return True


# Bulk create users
# This accepts a list of dictionaries
# Example:
# [
#     {
#         'first_name': 'John',
#         'last_name': 'Doe',
#         ...
#     }
# ]
def create_users_bulk(data_list):
    # Successfully saved accounts
    saved_accounts = []

    # Users that already exist
    duplicate_users = []

    # Invalid or duplicate emails
    invalid_emails = []

    # Records with missing fields or invalid names
    failed_records = []

    try:
        # Loop through each user record from the request body
        for index, data in enumerate(data_list, start=1):

            # Step 1: Check required fields
            if not check_require_fields(data):
                failed_records.append({
                    'row': index,
                    'error': 'Missing or empty required fields'
                })
                continue

            # Step 2: Clean and prepare user input
            first_name = str(data.get('first_name', '')).strip()
            middle_name = str(data.get('middle_name', '')).strip()
            last_name = str(data.get('last_name', '')).strip()
            email = str(data.get('email', '')).strip()
            password = str(data.get('password', '')).strip()
            role = str(data.get('role', '')).strip().lower()

            # Step 3: Validate names
            # Names should not contain numbers
            if any(char.isdigit() for char in first_name):
                failed_records.append({
                    'row': index,
                    'error': f'Invalid first name: {first_name}'
                })
                continue

            if middle_name and any(char.isdigit() for char in middle_name):
                failed_records.append({
                    'row': index,
                    'error': f'Invalid middle name: {middle_name}'
                })
                continue

            if any(char.isdigit() for char in last_name):
                failed_records.append({
                    'row': index,
                    'error': f'Invalid last name: {last_name}'
                })
                continue

            # Step 4: Check if user already exists
            if check_user_exists(first_name, last_name):
                duplicate_users.append({
                    'row': index,
                    'name': f'{first_name} {last_name}'
                })
                continue

            # Step 5: Validate email format
            is_valid, email_or_error = is_valid_email(email)

            if not is_valid:
                invalid_emails.append({
                    'row': index,
                    'email': email,
                    'error': email_or_error
                })
                continue

            # If valid, use the normalized email returned by validator
            email = email_or_error

            # Step 6: Check if email already exists in database
            if check_email_exists(email):
                invalid_emails.append({
                    'row': index,
                    'email': email,
                    'error': 'Email already exists'
                })
                continue

            # Step 7: Create the profile record
            profile = Profiles(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                suffix=data.get('suffix'),
                birth_date=data.get('birth_date'),
                gender=data.get('gender')
            )
            profile.save()

            # Step 8: Create the user account record
            user = Users(
                profile_id=profile.id,
                email=email,
                password=hash_password(password)
            )
            user.save()

            # Step 9: Create the role mapping record
            user_role = UserRoles(
                user_id=user.id,
                role_id=check_user_role(role)
            )
            user_role.save()

            # Step 10: Create additional role-specific record
            if role == 'student':
                student = Students(
                    profile_id=profile.id,
                    year_level=data.get('year_level') or 0
                )
                student.save()

            elif role == 'instructor':
                instructor = Instructors(
                    profile_id=profile.id
                )
                instructor.save()

            else:
                failed_records.append({
                    'row': index,
                    'error': f'Invalid role: {role}'
                })
                continue

            # Step 11: Store successful account in response list
            saved_accounts.append({
                'id': profile.id,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': email,
                'role': role
            })

        # Step 12: Return all results
        return {
            'success': True,
            'saved_accounts': saved_accounts,
            'duplicate_users': duplicate_users,
            'invalid_emails': invalid_emails,
            'failed_records': failed_records
        }

    except Exception as e:
        return {
            'success': False,
            'message': 'Something went wrong while processing bulk users',
            'error': str(e)
        }

