import pytz
from flask import Blueprint, request, jsonify
from models import Loan, Book, User
from db import db
from datetime import datetime, timedelta
from flask_cors import CORS
# Initialize Blueprint
loan_routes = Blueprint('loan', __name__)
CORS(loan_routes)

@loan_routes.route('/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    data = request.get_json()

    # Ensure the loan exists
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    # Update loan fields
    loan.book_id = data.get('book_id', loan.book_id)
    loan.user_id = data.get('user_id', loan.user_id)
    loan.loan_date = data.get('loan_date', loan.loan_date)
    loan.title = data.get('title', loan.title)
    loan.return_date = data.get('return_date', loan.return_date)
    if loan.book_id:
        book = Book.query.get(loan.book_id)
    if book:
        loan.title = book.title 
    # Handle clearing of the date_returned (marking the loan as ongoing)
    loan_date_returned = data.get('date_returned', None)

    # Check if date_returned is an empty string and set it to None
    if loan_date_returned == '':
        loan_date_returned = None

    if loan_date_returned is None:
        loan.date_returned = None
    else:
        loan.date_returned = loan_date_returned  # If provided, set it as usual


    # Handle increasing quantity based on date_returned
    book = Book.query.get(loan.book_id)
    if book:
        if loan.date_returned:  # If date_returned is set (book returned)
            book.quantity += 1  # Increase quantity when the book is returned
        else:  # If date_returned is cleared or not set (book still loaned out)
            book.quantity -= 1  # Decrease quantity when the book is loaned out

    try:
        db.session.commit()
        return jsonify({"message": "Loan updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating loan', 'error': str(e)}), 500


@loan_routes.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    
    # Validate required fields
    if 'user_id' not in data or 'book_id' not in data:
        return jsonify({'message': 'user_id, book_id, and return_date are required'}), 400
    
    # Ensure the book exists and is available
    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    if book.quantity <= 0:  # Check if the book has any available copies left
        return jsonify({'message': 'No copies available for borrowing'}), 400
    
    # Ensure the user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Check if the user has already borrowed the book and has not returned it
    active_loan = Loan.query.filter_by(user_id=data['user_id'], book_id=data['book_id'], date_returned=None).first()
    if active_loan:
        return jsonify({
        'success': False, 
        'message': 'You need to return the first copy of the book before borrowing it again.'
        }), 400
    
    serbia_tz = pytz.timezone('Europe/Belgrade')
    
    # Create new loan record
    loan = Loan(
        user_id=data['user_id'],
        book_id=data['book_id'],
        title=book.title,
        loan_date=datetime.now(serbia_tz),
        return_date=datetime.now(serbia_tz) + timedelta(days=30)
    )
    
    # Update the book's quantity
    book.quantity -= 1  # Decrease the quantity by 1

    # If no copies are left, mark the book as unavailable
    if book.quantity == 0:
        book.available = False

    try:
        db.session.add(loan)
        db.session.commit()
        return jsonify({"success": True, "message": "Book borrowed successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error borrowing book', 'error': str(e)}), 500

# Get all loans
@loan_routes.route('/', methods=['GET'])
def get_loans():
    loans = Loan.query.all()

    # Return list of loans including the date_returned field
    return jsonify([{
        'id': loan.id,
        'title': loan.title,
        'user_id': loan.user_id,
        'book_id': loan.book_id,
        'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
        'return_date': loan.return_date.strftime('%Y-%m-%d'),
        'date_returned': loan.date_returned.strftime('%Y-%m-%d') if loan.date_returned else None
    } for loan in loans]), 200

# Get a specific loan by ID
@loan_routes.route('/<int:id>', methods=['GET'])
def get_loan(id):
    loan = Loan.query.get(id)

    if loan:
        return jsonify({
            'id': loan.id,
            'user_id': loan.user_id,
            'book_id': loan.book_id,
            'title': loan.title,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d'),
            'date_returned': loan.date_returned.strftime('%Y-%m-%d') if loan.date_returned else None
        }), 200
    else:
        return jsonify({'message': 'Loan not found'}), 404

# Return a borrowed book
@loan_routes.route('/return/<int:id>', methods=['PUT'])
def return_book(id):
    loan = Loan.query.get(id)
    
    if not loan:
        return jsonify({'message': 'Loan not found'}), 404
    
    # Ensure the book is returned on or before the return date
    loan.book.available = True  # Mark the book as available again
    loan.date_returned = datetime.utcnow()
    
    # Increase the book's quantity by 1
    loan.book.quantity += 1

    # If the quantity is greater than 0, ensure the book is marked as available
    if loan.book.quantity > 0:
        loan.book.available = True
    else:
        loan.book.available = False  # If no copies left, mark as unavailable
    
    try:
        db.session.commit()

        # Return the updated loan data including the date_returned
        updated_loan = {
            'id': loan.id,
            'title': loan.book.title,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'date_returned': loan.date_returned.strftime('%Y-%m-%d') if loan.date_returned else None,
        }

        return jsonify(updated_loan), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error returning book', 'error': str(e)}), 500

# Get all loans for a specific user
@loan_routes.route('/user/<int:user_id>', methods=['GET'])
def get_loans_for_user(user_id):
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Query for loans, sorted by loan_date in descending order (newest first)
    loans_query = Loan.query.filter_by(user_id=user_id).order_by(Loan.loan_date.desc()).paginate(page=page, per_page=limit, error_out=False)
    
    loans = loans_query.items
    total_pages = loans_query.pages

    loan_data = [{
        'id': loan.id,
        'title': loan.book.title if loan.book else "Unknown",
        'loan_date': loan.loan_date,
        'date_returned': loan.date_returned,
    } for loan in loans]

    return jsonify({
        'loans': loan_data,
        'totalPages': total_pages,
    })
@loan_routes.route('/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        db.session.delete(loan)
        db.session.commit()
        return jsonify({'message': 'Loan deleted successfully'}), 200
    return jsonify({'message': 'Loan not found'}), 404

@loan_routes.route('/add', methods=['POST'])
def add_loan():
    try:
        data = request.json

        # Input validation
        required_fields = ['book_id', 'user_id', 'loan_date', 'return_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Check if book exists
        book = Book.query.get(data['book_id'])
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Check if the book is available
        if book.quantity <= 0:
            return jsonify({'error': 'Book not available for loan'}), 400

        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Set date_returned to None if not provided
        date_returned = data.get('date_returned', None)
        if date_returned == "":
            date_returned = None
        # Create and save new loan
        new_loan = Loan(
            book_id=data['book_id'],
            user_id=data['user_id'],
            loan_date=data['loan_date'],
            return_date=data['return_date'],
            title=data['title'],
            date_returned=date_returned
        )

        # Update book quantity
        book.quantity -= 1

        db.session.add(new_loan)
        db.session.commit()

        return jsonify({
            'message': 'Loan added successfully',
            'loan': {
                'id': new_loan.id,
                'book_id': new_loan.book_id,
                'user_id': new_loan.user_id,
                'loan_date': new_loan.loan_date,
                'return_date': new_loan.return_date,
                'date_returned': new_loan.date_returned,
                'title':new_loan.title
            }
        }), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'error': str(e)}), 500
