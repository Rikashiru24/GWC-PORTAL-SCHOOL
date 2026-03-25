# app/__init__.py
from flask import Flask
from config import Config
from app.api.auth import api_bp
from .models import (
    Profiles, Students, Instructors, Subjects, Attendance,
    Grades, SubjectsInstructors, Classes, Enrollments,
    Users, Roles, Permissions, UserRoles, RolePermissions
)

def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)
    app.register_blueprint(api_bp)
    # Create tables when app starts (only once)
    # with app.app_context():
    #     create_all_tables()
    return app

def create_all_tables():
    '''Create all tables in correct order'''
    print('Initializing database...')

    # Core tables
    Profiles.create_table()
    Subjects.create_table()
    Roles.create_table()
    Permissions.create_table()

    # Dependent tables
    Students.create_table()
    Instructors.create_table()
    Users.create_table()

    # Junction tables
    SubjectsInstructors.create_table()
    Classes.create_table()

    # Final tables
    Attendance.create_table()
    Grades.create_table()
    Enrollments.create_table()
    UserRoles.create_table()
    RolePermissions.create_table()

    print('Database initialized successfully!')
