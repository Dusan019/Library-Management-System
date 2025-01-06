# user_routes.py

from flask import Blueprint, request, jsonify
from models import User,Loan
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from db import db

user_routes = Blueprint('user', __name__)

# Route for getting user details
@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Return user details, including email, name, and last_name
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,       # Adding email
        'name': user.name,         # Adding name
        'last_name': user.last_name, # Adding last name
        'role': user.role
    }
    return jsonify(user_data)


# Route for updating user information
@user_routes.route('/<int:user_id>/update', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    try:
        # Update user information
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        user.last_name = data.get('last_name', user.last_name)
        user.username = data.get('username', user.username)

        # If password is provided, hash it and update
        if 'password' in data:
            user.password = generate_password_hash(data['password'], method='sha256')
        
        # Update role if provided
        if 'role' in data:
            user.role = data['role']
        
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Route for deleting a user
@user_routes.route('/<int:user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
    # Find the user
    user = User.query.get_or_404(user_id)

    # Check for outstanding loans
    outstanding_loans = Loan.query.filter_by(user_id=user_id, date_returned=None).all()
    
    if outstanding_loans:
        return jsonify({"message": "User cannot be deleted due to outstanding loans"}), 400

    # Proceed to delete the user
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting user", "error": str(e)}), 500

# Route for getting all users (admin only)
@user_routes.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,  # Add email
        'name': user.name,  # Add name
        'last_name': user.last_name,  # Add last_name
        'role': user.role
    } for user in users]
    
    return jsonify(users_list)


@user_routes.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()  # Get JSON data from the request
    
    # Extract data from the request
    username = data.get('username')
    password = data.get('password')  # Password should be provided
    email = data.get('email')
    name = data.get('name')
    last_name = data.get('last_name')
    role = data.get('role')
    
    # Validate required fields
    if not username or not password or not email or not name or not last_name or not role:
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400
    
    # Hash the password before saving it
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(
        username=username,
        password=hashed_password,
        email=email,
        name=name,
        last_name=last_name,
        role=role
    )
    
    # Add user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # Return success message
    return jsonify({'message': 'User added successfully', 'user': {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'name': new_user.name,
        'last_name': new_user.last_name,
        'role': new_user.role
    }}), 201


# Route for changing user password
@user_routes.route('/<int:user_id>/change-password', methods=['PUT'])
def change_password(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404

    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password:
        return jsonify({"message": "Current password is required"}), 400

    # Check if the current password matches the one stored in the database
    if not check_password_hash(user.password, current_password):
        return jsonify({"message": "Current password is incorrect"}), 400
    
    if not new_password:
        return jsonify({"message": "New password is required"}), 400

    try:
        # Update the password after hashing it
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({"message": "Password changed successfully"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500