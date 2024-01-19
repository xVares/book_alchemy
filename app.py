from datetime import date, datetime
from flask import Flask, request, render_template, url_for
from data_models import db, Author, Book

# Configure Flask with SQLite db using Flask-SQLAlchemy
app = Flask(__name__)
db.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/library.sqlite"


@app.route("/")
def home():
    books = db.session.query(Book).order_by(Book.title.asc()).distinct().all()
    return render_template("home.html", books=books)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "GET":
        return render_template("add_author.html")

    if request.method == "POST":
        name = request.form.get("name")
        form_birthdate = request.form.get("birthdate")
        birthdate = datetime.strptime(form_birthdate, "%Y-%m-%d").date()
        form_date_of_death = request.form.get("date_of_death")
        date_of_death = datetime.strptime(form_date_of_death,
                                          "%Y-%m-%d").date()

        try:
            # Assuming 'birthdate' and 'date_of_death' are valid date strings
            new_author = Author(name=name, birthdate=birthdate, date_of_death=date_of_death)

            db.session.add(new_author)
            db.session.commit()

            # Render success page
            return render_template("adding_successful.html", author_added=True)

        except ValueError:
            # Handle the case where birthdate or date_of_death is not a valid date
            return render_template("error.html", message="Invalid date format")

    # Handle other HTTP methods or unexpected scenarios
    return render_template("error.html", message="Invalid request method or unexpected scenario")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        # Get all Author names in desc order
        authors = db.session.query(Author).order_by(Author.name.asc()).distinct().all()
        print(authors)
        return render_template("add_book.html", authors=authors)

    if request.method == "POST":
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        form_publication_year = request.form.get("publication_year")
        publication_year = datetime.strptime(form_publication_year,
                                             "%Y-%m-%d").date()
        author_id = request.form.get("author")

        # Ensure that author_id is an integer
        try:
            author_id = int(author_id)
        except ValueError:
            # Handle the case where author_id is not a valid integer
            return render_template("error.html", message="Invalid author selection")

        new_book = Book(isbn=isbn, title=title, publication_year=publication_year,
                        author_id=author_id)

        db.session.add(new_book)
        db.session.commit()

        # Render success page
        return render_template("adding_successful.html", book_added=True)

    # Handle other HTTP methods or unexpected scenarios
    return render_template("error.html", message="Invalid request method or unexpected scenario")


if __name__ == '__main__':
    app.run(debug=True)

    # with app.app_context():
    #     db.create_all()
