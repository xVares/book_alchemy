# Library Management System

This is a simple Flask web application for managing a library's book and author information. The application provides functionality to view, add, search, and delete books and authors.

## Features

- **Home Page (Library):** Displays a list of books sorted by title or author. Provides an option to search for books by title or author.

- **Add Author:** Allows users to add a new author with details such as name, birthdate, and date of death (optional).

- **Search Functionality:** Easily find specific books or authors using the search feature on the home page. The search is case-insensitive and supports partial matches.

- **Add Book:** Enables users to add a new book with details including title, ISBN, publication year, and the associated author.

- **Delete Book:** Provides a way to delete a specific book from the library. If the author of the book has no other books in the library, the author is also deleted.


## Getting Started

1. Clone the repository: `git clone [repository_url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`
4. Open your browser and navigate to http://127.0.0.1:5000/

## Dependencies

- Flask
- Flask-SQLAlchemy
- SQLAlchemy


## Additional Notes

- The application uses SQLite as the database, and the database file is named "library.sqlite."
- Error handling is implemented to manage cases where duplicate books are added or invalid dates are entered.
- The styling of the application is kept simple and utilizes plain HTML without the use of CSS. 