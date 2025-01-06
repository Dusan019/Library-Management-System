from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from db import db
import os
from config import Config
from auth_routes import auth_routes
from user_routes import user_routes
from book_routes import book_routes
from loan_routes import loan_routes


# Initialize the Flask app
app = Flask(__name__)


# Initialize extensions
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}  # Allowed file types
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Backend folder
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'public', 'images')  # Relative path to frontend/public/images
app.config['UPLOAD_FOLDER'] = os.path.abspath(FRONTEND_DIR)

# CORS handling for OPTIONS requests (preflight)
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight passed'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response, 200

# JWT protection for all routes except login/register
@app.before_request
def check_authentication():
    if request.endpoint not in ['auth.login', 'auth.register']:  # Don't apply to login/register endpoints
        jwt_required()(lambda: None)  # Apply the jwt_required decorator

# Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(book_routes, url_prefix='/books')
app.register_blueprint(loan_routes, url_prefix='/loans')

if __name__ == '__main__':
    app.run(debug=True)
