from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    def __str__(self):
        return f"Author: {self.name}, ID: {self.id}"

    def __repr__(self):
        return (f"<Author(id={self.id}, name={self.name}, "
                f"birth_date={self.birth_date}, "
                f"date_of_death={self.date_of_death})>")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return (f"<Book(id={self.id}, isbn={self.isbn}, "
                f"title={self.title}, publication_year={self.publication_year}, "
                f"author_id={self.author_id})>")

    def __str__(self):
        return (f"Book: {self.title}, ISBN: {self.isbn}, "
                f"Year: {self.publication_year}, Author ID: {self.author_id}")
