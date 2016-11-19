#!/usr/bin/env python3

from flask import Flask
app = Flask(__name__)


@app.route('/')
def show_homepage():
    return "Book genres and recent book additions"


@app.route('/genre/<string:genre>/')
def show_genre(genre):
    return "Genre {} books: ...".format(genre)


@app.route('/genre/<string:genre>/new-book')
def show_add_book(genre):
    return "Adding book to genre {}".format(genre)


@app.route('/book/<string:book_title>')
def show_book(book_title):
    return "Information about book {}".format(book_title)


@app.route('/book/<string:book_title>/delete')
def show_delete_book(book_title):
    return "Are you sure you wish to delete a book {}?".format(book_title)


@app.route('/book/<string:book_title>/edit')
def show_edit_book(book_title):
    return "Editing book {}".format(book_title)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
