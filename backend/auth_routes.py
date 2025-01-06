from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from db import db
import jwt
from datetime import datetime, timedelta
from config import Config
from flask_cors import CORS
# Initialize Blueprint
auth_routes = Blueprint('auth', __name__)
CORS(auth_routes)
# Function to generate JWT Token
def generate_jwt_token(user_id: int, role: str) -> str:
    """
    Generates a JWT token with the user_id and role.
    """
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': expiration
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

# Route for User Registration
@auth_routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    # Ensure required fields are provided
    if not data.get('username') or not data.get('password') or not data.get('email') or not data.get('name') or not data.get('last_name'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'])
    
    # Create new user with the default role 'member'
    new_user = User(
        username=data['username'],
        password=hashed_password,
        email=data['email'],
        name=data['name'],
        last_name=data['last_name'],
        role='member'  # Default to 'member' role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Route for User Login (returns JWT Token)
@auth_routes.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Check if username and password are provided
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required'}), 400

    # Get user from the database
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        # Generate JWT token
        token = generate_jwt_token(user.id, user.role)
        return jsonify({'message': 'Login successful', 'token': token, 'username': user.username,'user_id': user.id}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Route for checking if user is logged in (using JWT)
@auth_routes.route('/validate', methods=['GET'])
def validate_user():
    token = request.headers.get('Authorization')  # Expecting token in the Authorization header

    if not token:
        return jsonify({'message': 'Token is missing'}), 400

    try:
        # Remove "Bearer " from token if included
        if token.startswith("Bearer "):
            token = token[7:]

        # Decode the JWT token
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return jsonify({'message': 'Token is valid', 'user_id': payload['user_id'], 'role': payload['role']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
