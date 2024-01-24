from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect
from data_models import db, Author, Book
from sqlalchemy.exc import IntegrityError

# Configure Flask with SQLite db using Flask-SQLAlchemy
app = Flask(__name__)
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/library.sqlite"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        # Get sort parameter from request, default to sorting by title
        sort_by = request.args.get("sort_by", "title")

        # Define sort order based on parameter
        if sort_by == "title":
            order_by = Book.title.asc()
        elif sort_by == "author":
            order_by = Author.name.asc()
        else:
            # Default to sorting by title if an invalid parameter is provided
            order_by = Book.title.asc()

        # Join tables, apply sorting, and retrieve the results
        joined_books = db.session.query(Book, Author) \
            .join(Author, Book.author_id == Author.id) \
            .order_by(order_by).all()

        return render_template("home.html", books=joined_books)

    if request.method == "POST":
        # Get the search query from the form
        search_query = request.form.get("search_query", "")

        # Perform case-insensitive search on book title and author name
        search_results = db.session.query(Book, Author) \
            .join(Author, Book.author_id == Author.id) \
            .filter(db.or_(Book.title.ilike(f"%{search_query}%"),
                           Author.name.ilike(f"%{search_query}%"))).all()

        if not search_results:
            # No results found, display a message
            return render_template("home.html", books=[], no_results=True,
                                   search_query=search_query)

        # Display search results
        return render_template("home.html", books=search_results, no_results=False,
                               search_query=search_query)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "GET":
        return render_template("add_author.html")

    # Get author name, birthdate and date of death from form
    if request.method == "POST":
        name = request.form.get("name")
        form_birthdate = request.form.get("birthdate")
        form_date_of_death = request.form.get("date_of_death")

        try:
            birthdate = datetime.strptime(form_birthdate, "%Y-%m-%d").date()

            # If author has date of death -> parse form data to date
            if form_date_of_death:
                date_of_death = datetime.strptime(form_date_of_death, "%Y-%m-%d").date()
            else:
                date_of_death = None

            # instantiate new Author object
            new_author = Author(name=name, birthdate=birthdate, date_of_death=date_of_death)

            # Add new Author to database
            db.session.add(new_author)
            db.session.commit()

            # Render success page
            return render_template("adding_successful.html", author_added=True)

        except ValueError:
            # Handle case where birthdate or date_of_death is not a valid date
            return render_template("error.html", message="Invalid date format")

    # Handle other HTTP methods or unexpected scenarios
    return render_template("error.html", message="Invalid request method or unexpected scenario")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        # Get all Author names in desc order
        authors = db.session.query(Author).order_by(Author.name.asc()).distinct().all()
        return render_template("add_book.html", authors=authors)

    if request.method == "POST":
        try:
            title = request.form.get("title")
            isbn = request.form.get("isbn")
            publication_year = request.form.get("publication_year")
            author_id = request.form.get("author")

            new_book = Book(isbn=isbn,
                            title=title,
                            publication_year=publication_year,
                            author_id=author_id)

            db.session.add(new_book)
            db.session.commit()

            # Render success page
            return render_template("adding_successful.html", book_added=True)

        # Handle case where book is already in the database
        except IntegrityError:
            return render_template("error.html", message="The book is already in the database")


@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    # Get the book to delete
    book = Book.query.get_or_404(book_id)

    # Check if author of the book has only this book in the library
    author = book.author
    db.session.delete(book)

    if author and Book.query.filter_by(author_id=author.id).count() == 0:
        db.session.delete(author)

    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
