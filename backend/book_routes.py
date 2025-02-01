from flask import Blueprint, request, jsonify,current_app
from models import Book
from werkzeug.utils import secure_filename
from db import db
import os
from flask_cors import CORS
# Initialize Blueprint
book_routes = Blueprint('book', __name__)

CORS(book_routes)
# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@book_routes.route('/add', methods=['POST'])
def add_book():
    data = request.form  
    print(f"Received data: {data}")

    # Check and convert 'available' to boolean if it's a string, otherwise leave it as is
    available = data.get('available', 'true')
    if isinstance(available, str):
        available = available.lower() == 'true'

    # Get quantity from the request, default to 0 if not provided
    quantity = data.get('quantity', 0)
    
    # Validate required fields
    if 'title' not in data or 'author' not in data:
        return jsonify({'message': 'Title and author are required'}), 400

    # Handle the image upload
    image_file = request.files.get('image')  # 'image' is the key used in the form
    image_url = None

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        # Save the image to the correct folder
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Save the image file
        image_file.save(image_path)
        
       
        image_url = f"images/{filename}" 
    # Create new book
    new_book = Book(
        title=data['title'],
        author=data['author'],
        available=available,
        quantity=quantity,
        image_url=image_url
    )

    try:
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error adding book', 'error': str(e)}), 500
    
@book_routes.route('/<int:book_id>/update-availability', methods=['PUT'])
def update_book_availability(book_id):
    try:
        book = Book.query.get(book_id)
        if book:
            book.available = True  # Mark the book as available
            db.session.commit()
            return jsonify({'message': 'Book availability updated successfully'}), 200
        else:
            return jsonify({'message': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Get all books
@book_routes.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()

    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'available': book.available,
        'quantity': book.quantity,
        'image_url': book.image_url  
    } for book in books]), 200

# Get a specific book by ID
@book_routes.route('/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)

    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'available': book.available,
            'quantity': book.quantity,
            'image_url': book.image_url   
        }), 200
    else:
        return jsonify({'message': 'Book not found'}), 404

# Update a book's details
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os

@book_routes.route('/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({'message': 'Book not found'}), 404

    
    title = request.form.get('title')
    author = request.form.get('author')
    quantity = request.form.get('quantity')
    image = request.files.get('image')  

    # Update book details if provided
    if title:
        book.title = title
    if author:
        book.author = author
    if quantity:
        book.quantity = int(quantity)  # Make sure it's an integer
    if image:
        # Handle the image upload
        if allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)  # Use the same upload folder
            image.save(image_path)
            book.image_url = f"images/{image_filename}"  # Save the relative image path in the database

    try:
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating book', 'error': str(e)}), 500

@book_routes.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    if query:
        # Case-insensitive search for books that start with the search term
        books = Book.query.filter(Book.title.ilike(f'{query}%')).all()
        return jsonify({'books': [book.to_dict() for book in books]})
    return jsonify({'books': []})

# Delete a book by ID
@book_routes.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Check if the book has active loans (loans where date_returned is NULL)
    active_loans = any(loan.date_returned is None for loan in book.loans)
    print(active_loans)
    if active_loans:
        return jsonify({'message': 'Cannot delete a book with active loans'}), 400

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting book', 'error': str(e)}), 500
