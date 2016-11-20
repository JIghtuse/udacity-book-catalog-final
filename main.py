#!/usr/bin/env python3

import logging
import re
from flask import Flask, render_template, request, redirect, url_for, abort
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common import DATABASE_FILENAME
from database_setup import Base, Genre, Book

BOOK_TITLE_RE = re.compile(r'^[-0-9a-zA-Z,;. ]*$')

app = Flask(__name__)

engine = create_engine("sqlite:///" + DATABASE_FILENAME)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_genre_id(genre_name):
    if genre_name is None:
        return None
    genre = session.query(Genre).filter_by(name=genre_name)
    if genre.count() == 0:
        logging.warning("Missing genre requested: {}".format(genre_name))
        return None
    return genre.one().id


def get_book_by_title(book_title):
    book_id = book_title.split('-', maxsplit=1)[0]
    book = session.query(Book).filter_by(id=book_id)
    if book.count() == 0:
        logging.warning("Missing book URL requested: {}".format(book_title))
        return None
    return book.one()


@app.route('/')
def show_homepage():
    genres = session.query(Genre).all()
    recent_books = session.query(Book).limit(10)
    return render_template('homepage.html',
                           genres=genres, recent_books=recent_books)


@app.route('/genre/<string:genre>/')
def show_genre(genre):
    genre = session.query(Genre).filter_by(name=genre).one()
    genre_books = session.query(Book).filter_by(genre_id=genre.id)
    return render_template('genre.html',
                           genre=genre,
                           genre_books=genre_books)


@app.route('/genre/<string:genre>/json')
def show_genre_json(genre):
    genre = session.query(Genre).filter_by(name=genre).one()
    genre_books = session.query(Book).filter_by(genre_id=genre.id)
    return jsonify(books=[book.serialize for book in genre_books])


@app.route('/genre/<string:genre>/new-book')
def show_add_book(genre):
    return render_template('book_new.html', genre_name=genre)


def validate_fields():
    """Validates form fields
    Returns (False, None) if some of the field is not valid,
    Returns (True, args_to_build_book) if all fields are valid """
    title = request.form.get('book-title')
    cover_url = request.form.get('book-image-url')
    cover_url_attribution = request.form.get('book-image-url-attribution')
    description = request.form.get('book-description')
    year = request.form.get('book-year')
    buy_url = request.form.get('book-buy-url')
    genre_name = request.form.get('book-genre')

    args = {'title': title,
            'cover_url': cover_url,
            'cover_url_attribution': cover_url_attribution,
            'description': description,
            'genre_id': get_genre_id(genre_name),
            'year': year,
            'buy_url': buy_url}

    if not all(args.values()):
        return False, None

    if not BOOK_TITLE_RE.match(args['title']):
        logging.warning("Suspicious title: {}".format(args['title']))
        return False, None

    return True, args


@app.route('/genre/<string:genre>/new-book', methods=["POST"])
def add_book_post_handler(genre):
    form_is_valid, book_args = validate_fields()
    if not form_is_valid:
        return abort(400)
    book = Book(**book_args)
    session.add(book)
    session.commit()
    return redirect(url_for('show_book', book_title=book.build_url()))


@app.route('/book/<string:book_title>')
def show_book(book_title):
    book = get_book_by_title(book_title)
    if book is None:
        return abort(404)
    return render_template('book.html', book=book)


@app.route('/book/<string:book_title>', methods=["POST"])
def book_post_handler(book_title):
    edit = request.form.get('book-edit')
    delete = request.form.get('book-delete')
    if edit is not None:
        return redirect(url_for('show_edit_book', book_title=book_title))
    elif delete is not None:
        return redirect(url_for('show_delete_book', book_title=book_title))
    else:
        logging.warning("Suspicious request: {} (no action)".format(request))


@app.route('/book/<string:book_title>/delete', methods=["GET", "POST"])
def show_delete_book(book_title):
    book = get_book_by_title(book_title)
    if book is None:
        return abort(404)
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        return redirect(url_for('show_homepage'))
    else:
        return render_template('book_delete.html', book=book)


@app.route('/book/<string:book_title>/edit', methods=["GET", "POST"])
def show_edit_book(book_title):
    book = get_book_by_title(book_title)
    if book is None:
        return abort(404)
    if request.method == 'POST':
        form_is_valid, book_args = validate_fields()
        if not form_is_valid:
            return abort(400)

        for key, value in book_args.items():
            setattr(book, key, value)

        session.add(book)
        session.commit()
        return redirect(url_for('show_book', book_title=book.build_url()))
    else:
        return render_template('book_edit.html', book=book)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8888)
