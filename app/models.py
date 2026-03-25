# app/models.py

from .db import get_db_connection


class Profiles:
    def __init__(self, id=None, first_name=None, middle_name=None, last_name=None, suffix=None, birth_date=None, gender=None, created_at=None, updated_at=None):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.suffix = suffix
        self.birth_date = birth_date
        self.gender = gender
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create_table():
        '''Create table if it doesnt exists'''
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tbl_profiles(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        first_name VARCHAR(200) NOT NULL,
                        middle_name VARCHAR(200) NULL,
                        last_name VARCHAR(200) NOT NULL,
                        suffix VARCHAR(10) NULL,
                        birth_date DATE NOT NULL,
                        gender VARCHAR(10) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Profiles: {e}')
        finally:
            cursor.close()
            conn.close()
        
    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_profiles( first_name, middle_name, last_name, suffix, birth_date, gender )
                VALUES( %s, %s, %s, %s, %s, %s ) 
            '''
            values = (self.first_name, self.middle_name, self.last_name, self.suffix, self.birth_date, self.gender)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving profile: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Students:
    def __init__(self, id=None, profile_id=None, year_level=None):
        self.id = id
        self.profile_id = profile_id
        self.year_level = year_level

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_students(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        profile_id INT,
                        year_level INT,
                        
                        CONSTRAINT fk_student_profile
                        FOREIGN KEY(profile_id) REFERENCES tbl_profiles(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Students: {e}')
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_students( profile_id, year_level )
                VALUES( %s, %s )        
            '''
            values = (self.profile_id, self.year_level)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving student: {e}')
            return False
        finally:
            conn.close()
            cursor.close()

class Instructors:
    def __init__(self, id=None, profile_id=None):
        self.id = id
        self.profile_id = profile_id

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_instructors(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        profile_id INT,
                        
                        CONSTRAINT fk_instructor_profile
                        FOREIGN KEY(profile_id) REFERENCES tbl_profiles(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Instructors: {e}')
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_instructors( profile_id )
                VALUES( %s )
            '''
            value = (self.profile_id,)
            cursor.execute(query, value)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback()  # Undo any partial changes if something went wrong
            print(f'Error saving instuctor: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Subjects:
    def __init__(self, id=None, subject_code=None, descriptive_title=None, units=None, department=None, year_level=None, semester=None):
        self.id = id
        self.subject_code = subject_code
        self.descriptive_title = descriptive_title
        self.units = units
        self.department = department
        self.year_level = year_level
        self.semester = semester

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_subjects(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        subject_code VARCHAR(50) NOT NULL,
                        descriptive_title VARCHAR(200) NOT NULL,
                        units INT NOT NULL,
                        department VARCHAR(50) NOT NULL,
                        year_level INT,
                        semester INT
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Subjects: {e}')
        finally:
            cursor.close()
            conn.close()
    
    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_subjects( subject_code, descriptive_title, units, department, year_level, semester )
                VALUES( %s, %s, %s, %s, %s, %s )
            '''
            values = (self.subject_code, self.descriptive_title, self.units, self.department, self.year_level, self.semester)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving subject: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Attendance:
    def __init__(self, id=None, student_id=None, instructor_id=None, subject_id=None,  present_day=None, absent_day=None, created_at=None):
        self.id = id
        self.student_id = student_id
        self.instructor_id = instructor_id
        self.subject_id = subject_id
        self.present_day = present_day
        self.absent_day = absent_day
        self.created_at = created_at

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_attendance(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        student_id INT,
                        instructor_id INT,
                        subject_id INT,
                        present_day INT NOT NULL,
                        absent_day INT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        
                        CONSTRAINT fk_attendance_student
                        FOREIGN KEY(student_id) REFERENCES tbl_students(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_attendance_instructor
                        FOREIGN KEY(instructor_id) REFERENCES tbl_instructors(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_attendance_subject
                        FOREIGN KEY(subject_id) REFERENCES tbl_subjects(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Attendance: {e}')
        finally:
            cursor.close()
            conn.close()
    
    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_attendance( student_id, instructor_id, subject_id, present_day, absent_day )
                VALUES( %s, %s, %s, %s, %s )
            '''
            values = (self.student_id, self.instructor_id, self.subject_id, self.present_day, self.absent_day)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving attendance: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Grades:
    def __init__(self, id=None, subject_id=None, prelim=None, midterm=None, semi_final=None, final=None, remarks=None):
        self.id = id
        self.subject_id = subject_id
        self.prelim = prelim
        self.midterm = midterm
        self.semi_final = semi_final
        self.final = final
        self.remarks = remarks

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_grades(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        subject_id INT,
                        prelim DECIMAL(5,2),
                        midterm DECIMAL(5,2),
                        semi_final DECIMAL(5,2),
                        final DECIMAL(5,2),
                        remarks VARCHAR(10),
                        
                        CONSTRAINT fk_grade_subject
                        FOREIGN KEY(subject_id) REFERENCES tbl_subjects(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Grades: {e}')
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_grades( subject_id, prelim, midterm, semi_final, final, remarks )
                VALUES( %s, %s, %s, %s, %s, %s )
            '''
            values = (self.subject_id, self.prelim, self.midterm, self.semi_final, self.final, self.remarks)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class SubjectsInstructors:
    def __init__(self, id=None, subject_id=None, instructor_id=None):
        self.id = id
        self.subject_id = subject_id
        self.instructor_id = instructor_id

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_subjects_instructors(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        subject_id INT,
                        instructor_id INT,
                        
                        CONSTRAINT fk_subject_intructor_subject
                        FOREIGN KEY(subject_id) REFERENCES tbl_subjects(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_subject_intructor_instructor
                        FOREIGN KEY(instructor_id) REFERENCES tbl_instructors(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table SubjectsInstructors: {e}')
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_subjects_instructors( subject_id, instructor_id )
                VALUES( %s, %s )
            '''
            values = (self.subject_id, self.instructor_id)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving Subject And Instructor: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Classes:
    def __init__(self, id=None, subject_id=None, instructor_id=None, semester=None, school_year=None, section=None):
        self.id = id
        self.subject_id = subject_id
        self.instructor_id = instructor_id
        self.semester = semester
        self.school_year = school_year
        self.section = section

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_classes(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        subject_id INT,
                        instructor_id INT,
                        semester INT NOT NULL,
                        school_year VARCHAR(8) NOT NULL,
                        section VARCHAR(15),
                        
                        CONSTRAINT fk_class_subject_id
                        FOREIGN KEY(subject_id) REFERENCES tbl_subjects(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_class_instructor
                        FOREIGN KEY(instructor_id) REFERENCES tbl_instructors(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Classes: {e}')
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_classes( subject_id, instructor_id, semester, school_year, section )
                VALUES( %s, %s, %s, %s, %s )
            '''
            values = (self.subject_id, self.instructor_id, self.semester, self.school_year, self.section)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving class: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Enrollments:
    def __init__(self, id=None, class_id=None, student_id=None):
        self.id = id
        self.class_id = class_id
        self.student_id = student_id

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_enrollments(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        class_id INT,
                        student_id INT,
                        
                        CONSTRAINT fk_enrollment_class
                        FOREIGN KEY(class_id) REFERENCES tbl_classes(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_enrollment_student
                        FOREIGN KEY(student_id) REFERENCES tbl_students(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Enrollments: {e}')
        finally:
            cursor.close()
            conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_enrollments( class_id, student_id )
                VALUES( %s, %s )
            '''
            values = (self.class_id, self.student_id)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback() # Undo any partial changes if something went wrong
            print(f'Error saving enrollment: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

'''Core RBAC Tables'''
class Users:
    def __init__(self, id=None, profile_id=None, email=None, password=None):
        self.id = id
        self.profile_id = profile_id
        self.email = email
        self.password = password
    
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_users(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        profile_id INT,
                        email VARCHAR(200) NOT NULL,
                        password VARCHAR(200) NOT NULL,
                        
                        CONSTRAINT fk_user_profile
                        FOREIGN KEY(profile_id) REFERENCES tbl_profiles(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Users: {e}')
        finally:
            cursor.close()
            conn.close()
    
    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_users( profile_id, email, password )
                VALUES( %s, %s, %s )
            '''
            values = (self.profile_id, self.email, self.password)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback()
            print(f'Error saving user: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Roles:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_roles(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(20) NOT NULL
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Roles: {e}')
        finally:    
            cursor.close()
            conn.close()

class UserRoles:
    def __init__(self, id=None, user_id=None, role_id=None):
        self.id = id
        self.user_id = user_id
        self.role_id = role_id

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_user_roles(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        user_id INT,
                        role_id INT,
                        
                        CONSTRAINT fk_user_role_user
                        FOREIGN KEY(user_id) REFERENCES tbl_users(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_user_role_role
                        FOREIGN KEY(role_id) REFERENCES tbl_roles(id) ON DELETE CASCADE          
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table UserRoles: {e}')
        finally:
            cursor.close()
            conn.close()
    
    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            query = '''
                INSERT INTO tbl_user_roles( user_id, role_id ) 
                VALUES( %s, %s )
            '''
            values = (self.user_id, self.role_id)
            cursor.execute(query, values)
            conn.commit()
            self.id = cursor.lastrowid
            return True
        except Exception as e:
            conn.rollback()
            print(f'error: {e}')
            return False
        finally:
            cursor.close()
            conn.close()

class Permissions:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
    
    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_permissions(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL
                    )
            ''')
            conn.commit()
        except Exception as e:
            print(f'Error saving table Permissions: {e}')
        finally:
            cursor.close()
            conn.close()

class RolePermissions:
    def __init__(self, role_id=None, permission_id=None):
        self.role_id = role_id
        self.permission_id = permission_id

    @staticmethod
    def create_table():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tbl_role_permissions(
                        role_id INT,
                        permission_id INT,
                        
                        CONSTRAINT fk_role_permission_role
                        FOREIGN KEY(role_id) REFERENCES tbl_roles(id) ON DELETE CASCADE,
                        
                        CONSTRAINT fk_role_permission_permission
                        FOREIGN KEY(permission_id) REFERENCES tbl_permissions(id) ON DELETE CASCADE
                    )
            ''')
            conn.commit()   
        except Exception as e:
            print(f'Error saving table RolePermissions: {e}')
        finally:
            cursor.close()
            conn.close()

