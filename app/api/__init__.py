# app/api/__init__.py

from flask import Blueprint
from flask_cors import CORS


api_bp = Blueprint('api', __name__, url_prefix='/api')
CORS(api_bp, origins="*")

from . import auth
from . import view
from . import students
