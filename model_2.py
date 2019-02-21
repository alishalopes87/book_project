"""Models and database functions for Books project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

class User(db.Model):
    """User of book_shelf website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)

    book_shelves = db.relationship("Book_shelf")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"

class Book(db.Model):
    """Book of book_shelf website"""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    title = db.Column(db.String(1000))
    isbn_10 = db.Column(db.String(100))
    isbn_13 = db.Column(db.String(100))
    subjects = db.Column(db.String(2000))
    
    subjects = db.relationship("Subject",
                                secondary="book_subjects",
                                backref="books")

    book_shelves = db.relationship('Book_shelf')

    def __repr__(self):
        """Provide helpful representation when printed"""

        return f"title={self.title} author={self.author}>"

class Author(db.Model):
    """Author table of webste"""

    __tablename__ ="authors"

    author_id = db.Column(db.Integer, primary_key=True)
    author_ol_id  = db.Column(db.String(100), unique=True)
    name= db.Column(db.String(1000))

    books = db.relationship("Book")

class Subject(db.Model):
    """Subject of book."""

    __tablename__ = "subjects"

    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(250), unique=True)

class BookSubjects(db.Model):
    """Subject of a specific book."""

    __tablename__ = "book_subjects"

    book_subject_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.book_id'),
                        nullable=False)
    subject_id = db.Column(db.Integer,
                            db.ForeignKey('subjects.subject_id'),
                            nullable=False)
                                         
class Book_shelf(db.Model):
    """Book_shelf of website"""

    __tablename__ = "book_shelves"

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))

        # Define relationship to user
    users = db.relationship("User")

    # Define relationship to book
    books = db.relationship("Book")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Book_shelf booking_id={self.booking_id} 
                   User-{self.user_id} 
                   book_id={self.book_id}"""

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///shelves'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")