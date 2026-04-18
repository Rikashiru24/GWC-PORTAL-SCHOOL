from flask import request, jsonify, current_app
from functools import wraps
import jwt
from datetime import datetime, timezone, timedelta

# Decorators
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]

            # Decode token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = {'id': data['user_id'], 'email': data['email']}
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return func(current_user, *args, **kwargs)
    return decorated


# generate token function
def generate_token(user_id, email):
    # 1. create payload. 
    # 'exp' stands for expiration time (Unix timestamp) of token
    # 'ia' issued at time = meaning

    now_utc = datetime.now(timezone.utc)

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": now_utc + timedelta(hours=24),
        "iat": now_utc
    }

    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return token
