#!/usr/bin/env python3

from flask import Flask, render_template
from data_stubs import genres, recent_books
app = Flask(__name__)


@app.route('/')
def show_homepage():
    return render_template('homepage.html',
                           genres=genres, recent_books=recent_books)


@app.route('/genre/<string:genre>/')
def show_genre(genre):
    return render_template('genre.html',
                           genre=genres[-1],
                           genre_books=recent_books)


@app.route('/genre/<string:genre>/new-book')
def show_add_book(genre):
    return render_template('book_new.html', genre_name=genre)


@app.route('/book/<string:book_title>')
def show_book(book_title):
    # TODO: get book from title
    book = recent_books[0]
    return render_template('book.html', book=book)


@app.route('/book/<string:book_title>/delete')
def show_delete_book(book_title):
    # TODO: get book from title
    book = recent_books[0]
    return render_template('book_delete.html', book=book)


@app.route('/book/<string:book_title>/edit')
def show_edit_book(book_title):
    # TODO: get book from title
    book = recent_books[0]
    return render_template('book_edit.html', book=book)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
