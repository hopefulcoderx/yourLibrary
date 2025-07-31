# 1. Import necessary libraries from Flask and Flask-SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_ # Import the 'or_' operator
import os

# 2. Initialize the Flask Application
app = Flask(__name__)

# 3. Configure the Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 4. Initialize the Database with our Flask App
db = SQLAlchemy(app)

# 5. Define the Database Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

# 6. Create the Database and Tables
with app.app_context():
    db.create_all()

# 7. Define the Routes

# Updated index route to only show books on search
@app.route('/')
def index():
    """
    Renders the homepage. Books are only displayed after a search is performed.
    """
    search_query = request.args.get('search')
    books = [] # Start with an empty list of books

    if search_query:
        # If a search query exists, filter the books and populate the list.
        # Use 'or_' to search in both title and author columns.
        # 'ilike' provides case-insensitive matching.
        search_pattern = f"%{search_query}%"
        books = Book.query.filter(
            or_(Book.title.ilike(search_pattern), Book.author.ilike(search_pattern))
        ).order_by(Book.title).all()

    # Pass the list of books (either empty or with search results) to the template.
    return render_template('index.html', books=books, search_query=search_query)


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

# 8. Run the Application
if __name__ == '__main__':
    app.run(debug=True)
