# root/app/utils/validation.py
from ..db import get_db_connection
from email_validator import validate_email, EmailNotValidError

# Check user first_name and last_name if it already exists
def check_user_exists(first_name, last_name):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = '''
            SELECT first_name, last_name
            FROM tbl_profiles
            WHERE first_name=%s AND last_name=%s LIMIT 1
        '''
        cursor.execute(query, (first_name, last_name))

        user_record = cursor.fetchone()
        if user_record:
            return True
        else:
            return False
    except Exception as e:
        print(f'error: {e}')
    finally:
        cursor.close()
        conn.close()

# Check email exists
def check_email_exists(email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = '''
            SELECT email
            FROM tbl_users
            WHERE email=%s LIMIT 1
        '''
        cursor.execute(query, (email,))
        user_email = cursor.fetchone()
        if user_email:
            return True
        else:
            return False
    except Exception as e:
        print(f'error: {e}')
    finally:
        cursor.close()
        conn.close()

# Check email if valid
def is_valid_email(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
        return True, email_info.normalized
    except EmailNotValidError as e:
        return False, str(e)
    
# return role id
def check_user_role(role):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''SELECT id FROM tbl_roles WHERE name=%s LIMIT 1''', (role,))
        result = cursor.fetchone()

        if result:
            return result['id']  # Access the first column (id)
        return None
    except Exception as e:
        print(f'Error fetching role: {e}')
        return None
    finally:
        cursor.close()
        conn.close()
