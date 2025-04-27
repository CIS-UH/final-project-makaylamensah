from database import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'available' or 'unavailable'

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    passwordhash = db.Column(db.String(255), nullable=False)  # Hashed password

class BorrowingRecord(db.Model):
    __tablename__ = 'borrowingrecords'
    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    customerid = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    borrowdate = db.Column(db.Date, default=datetime.utcnow)
    returndate = db.Column(db.Date, nullable=True)
    late_fee = db.Column(db.Float, default=0.0)

    book = db.relationship('Book', backref='borrowings')
    customer = db.relationship('Customer', backref='borrowings')
