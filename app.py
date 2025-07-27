from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    author = db.Column(db.String(100), nullable=False) 
  
    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    Renders the homepage which displays all books in the library.
    """
    books = Book.query.order_by(Book.title).all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    """
    Handles the form submission for adding a new book.
    """
    title = request.form.get('title')
    author = request.form.get('author')

    if title and author:
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_book(id):
    """
    Deletes a book from the database based on its ID.
    """
    book_to_delete = Book.query.get(id)
    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':

    app.run(debug=True)