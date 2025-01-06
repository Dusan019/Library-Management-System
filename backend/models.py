from db import db

# Users Table Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('member', 'librarian'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Ensure email is defined
    name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    # Relationships
    loans = db.relationship('Loan', backref='user', lazy=True,cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

# Books Table Model
class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=0)  # Add quantity field
    image_url = db.Column(db.String(255), nullable=True)  # Add image_url field

    # Relationships
    loans = db.relationship('Loan', backref='book', cascade='all, delete-orphan')
    def to_dict(self):
        """Converts the Book object to a dictionary for JSON response."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'available': self.available,
            'quantity':self.quantity,
            'image_url': self.image_url
        }

    def __repr__(self):
        return f'<Book {self.title}>'

# Loans Table Model
class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    date_returned = db.Column(db.DateTime,nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'loan_date': self.loan_date.isoformat() if self.loan_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'date_returned': self.date_returned.isoformat() if self.date_returned else None,
            'book': self.book.title if self.book else None,  # Assuming Book has a 'title' attribute
            'user': self.user.username if self.user else None,  # Assuming User has a 'username' attribute
        }
    def __repr__(self):
        return f'<Loan User {self.user_id} - Book {self.book_id}>'
