from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from models import Book, Customer, BorrowingRecord
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Youngkayla35!@cis2368spring.cqvqcae80duk.us-east-1.rds.amazonaws.com/librarydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db.init_app(app)

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

# --- Health Check ---
@app.route('/')
def home():
    return "Library System Backend Running!"

# --- CRUD APIs for Books ---
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'status': book.status
    } for book in books])

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        status='available'  # Default new book status
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

# --- CRUD APIs for Customers ---
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'firstname': customer.firstname,
        'lastname': customer.lastname,
        'email': customer.email
    } for customer in customers])

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_customer = Customer(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        passwordhash=hashed_password
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

# --- Borrow Book ---
@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.json
    book = Book.query.get(data['bookid'])
    customer = Customer.query.get(data['customerid'])

    if book.status != 'available':
        return jsonify({'error': 'Book not available'}), 400

    current_borrow = BorrowingRecord.query.filter_by(customerid=customer.id, returndate=None).first()
    if current_borrow:
        return jsonify({'error': 'Customer already has a borrowed book'}), 400

    borrow = BorrowingRecord(
        bookid=book.id,
        customerid=customer.id,
        borrowdate=datetime.utcnow()
    )
    book.status = 'unavailable'
    db.session.add(borrow)
    db.session.commit()

    return jsonify({'message': 'Borrowing recorded successfully'}), 201

# --- Return Book ---
@app.route('/return/<int:borrow_id>', methods=['PUT'])
def return_book(borrow_id):
    borrow = BorrowingRecord.query.get(borrow_id)
    if not borrow:
        return jsonify({'error': 'Borrowing record not found'}), 404

    borrow.returndate = datetime.utcnow()
    days_borrowed = (borrow.returndate - borrow.borrowdate).days
    borrow.late_fee = max(0, days_borrowed - 10) * 1.0

    book = Book.query.get(borrow.bookid)
    book.status = 'available'

    db.session.commit()

    return jsonify({
        'message': 'Book returned successfully',
        'late_fee': borrow.late_fee
    }), 200

# --- Run the server ---
if __name__ == '__main__':
    app.run(debug=True)

