#!/usr/bin/env python3

import json
import logging
import random
import string
import re
import hashlib
from urllib.parse import urlencode
from flask import Flask, render_template, request, redirect, url_for, abort
from flask import jsonify, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common import DATABASE_PATH
from database_setup import Base, Genre, Book, User
from secrets import FLASH_SECRET
from oauth import OAUTH_PROVIDER_DATA
import requests
from requests.auth import HTTPBasicAuth

USERAGENT = "udacity-book-catalog 0.1"
BOOK_TITLE_RE = re.compile(r'^[\w\d,;. ]*$', re.UNICODE)

app = Flask(__name__)
app.secret_key = FLASH_SECRET

engine = create_engine(DATABASE_PATH)
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
                           genres=genres, recent_books=recent_books,
                           login_session=login_session)


@app.route('/json')
def show_homepage_json():
    genres = session.query(Genre).all()
    recent_books = session.query(Book).limit(10)
    for book in session.query(Book).limit(10):
        logging.warning(book.user)
    return jsonify(genres=[genre.serialize for genre in genres],
                   recent_books=[book.serialize for book in recent_books])


@app.route('/genre/<string:genre>/')
def show_genre(genre):
    genre = session.query(Genre).filter_by(name=genre).one()
    genre_books = session.query(Book).filter_by(genre_id=genre.id)
    return render_template('genre.html',
                           genre=genre,
                           genre_books=genre_books,
                           login_session=login_session)


@app.route('/genre/<string:genre>/json')
def show_genre_json(genre):
    genre = session.query(Genre).filter_by(name=genre).one()
    genre_books = session.query(Book).filter_by(genre_id=genre.id)
    return jsonify(books=[book.serialize for book in genre_books])


@app.route('/genre/<string:genre>/new-book')
def show_add_book(genre):
    if 'user' not in login_session:
        flash("Please login to add new books", 'error')
        return redirect(url_for('show_login'))
    return render_template('book_new.html', genre_name=genre,
                           login_session=login_session)


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
    if 'user' not in login_session:
        flash("Please login to add new books", 'error')
        return redirect(url_for('show_login'))
    form_is_valid, book_args = validate_fields()
    if not form_is_valid:
        return abort(400)
    book = Book(**book_args, user_id=login_session['user_id'])
    session.add(book)
    session.commit()
    flash("Book successfully added")
    return redirect(url_for('show_book', book_title=book.build_url()))


@app.route('/book/<string:book_title>')
def show_book(book_title):
    book = get_book_by_title(book_title)
    if book is None:
        return abort(404)
    return render_template('book.html', book=book, login_session=login_session)


@app.route('/book/<string:book_title>/json')
def show_book_json(book_title):
    book = get_book_by_title(book_title)
    if book is None:
        return abort(404)
    return jsonify(book=book.serialize)


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
    if 'user' not in login_session:
        flash("Please login to delete books", 'error')
        return redirect(url_for('show_login'))
    book = get_book_by_title(book_title)
    if book is None:
        return abort(404)
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash("Book successfully deleted")
        return redirect(url_for('show_homepage'))
    else:
        return render_template('book_delete.html', book=book,
                               login_session=login_session)


@app.route('/book/<string:book_title>/edit', methods=["GET", "POST"])
def show_edit_book(book_title):
    if 'user' not in login_session:
        flash("Please login to edit books", 'error')
        return redirect(url_for('show_login'))
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
        flash("Book successfully updated")
        return redirect(url_for('show_book', book_title=book.build_url()))
    else:
        return render_template('book_edit.html', book=book,
                               login_session=login_session)


def make_auth_url(provider_name, provider_data):
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(32))
    login_session[provider_name] = {'state': state}
    params = {
        "client_id": provider_data['client_id'],
        "response_type": "code",
        "state": state,
        "redirect_uri": provider_data['redirect_uri'],
        "duration": "temporary",
        "scope": provider_data['scope'],
    }
    url = provider_data['auth_url'] + urlencode(params)
    return url


@app.route('/login')
def show_login():
    providers = []
    for provider in OAUTH_PROVIDER_DATA:
        providers.append({
            'name': provider,
            'auth_url': make_auth_url(provider, OAUTH_PROVIDER_DATA[provider])
        })
    return render_template('login.html', providers=providers,
                           login_session=login_session)


@app.route('/logout/<provider>')
def logout(provider):
    access_token = login_session[provider]['access_token']
    if access_token is None:
        return make_json_response("Current user not connected", 401)

    if provider not in OAUTH_PROVIDER_DATA:
        logging.warning("Missing provider {}".format(provider))
        return make_json_response("No such provider", 500)

    provider_data = OAUTH_PROVIDER_DATA[provider]

    headers = {
        "User-agent": USERAGENT,
    }

    try:
        if provider_data['revoke_method'] == 'GET':
            request_url = provider_data['revoke_url'] + "token=" + access_token
            response = requests.get(request_url, headers=headers)
        elif provider_data['revoke_method'] == 'POST':
            client_auth = HTTPBasicAuth(provider_data['client_id'],
                                        provider_data['client_secret'])

            headers = {
                "Accept": "application/json",
            }
            post_data = {
                "token": login_session[provider]['access_token'],
            }

            response = requests.post(
                provider_data['revoke_url'],
                data=post_data,
                auth=client_auth,
                headers=headers)
        else:
            response = requests.Response()
            response.status_code = 200

    except requests.exceptions.ConnectionError as e:
        flash(str(e), 'error')
        logging.exception("Failed logout")
        return redirect(url_for('show_homepage'))

    if response.status_code == 200 or response.status_code == 204:
        login_session[provider].clear()
        del login_session[provider]
        del login_session['user']
        del login_session['provider']
        del login_session['user_id']
        del login_session['avatar']

        flash("Logout successful")
        return redirect(url_for('show_homepage'))
    else:
        logging.warning(response.text)
        return make_json_response("Failed to revoke token for given user", 400)


def get_oauth_token(provider_data, code):
    client_auth = HTTPBasicAuth(provider_data['client_id'],
                                provider_data['client_secret'])
    post_data = {
        "code": code,
        "redirect_uri": provider_data['redirect_uri'],
        "grant_type": "authorization_code",
    }

    headers = {
        "Accept": "application/json",
    }

    response = requests.post(
        provider_data['access_token_url'],
        auth=client_auth,
        data=post_data,
        headers=headers)

    token_json = response.json()
    if 'error' in token_json:
        return None
    return token_json["access_token"]


def make_json_response(data, return_code):
    response = make_response(json.dumps(data), return_code)
    response.headers['Content-Type'] = 'application/json'
    return response


def retrieve_userinfo(token, provider_name, provider_data):
    headers = {
        "Authorization": provider_data['auth_header_name'] + " " + token,
        "User-agent": USERAGENT,
    }
    request_url = provider_data['oauth_url'] + provider_data['user_request']
    response = requests.get(request_url, headers=headers)
    user_json = response.json()
    if 'email' in user_json:
        login_session[provider_name]['email'] = user_json['email']

    username_field = provider_data['user_name_field']
    login_session[provider_name]['id'] = user_json['id']
    login_session[provider_name]['access_token'] = token
    login_session['provider'] = provider_name
    login_session['user'] = user_json[username_field]

    user_id = get_user_by_provider(login_session)
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    user = session.query(User).get(user_id)
    login_session['avatar'] = user.picture


@app.route('/callback/<provider>')
def sign_in_with_provider(provider):
    if provider not in OAUTH_PROVIDER_DATA:
        logging.warning("Missing provider {}".format(provider))
        return make_json_response("No such provider", 500)

    provider_data = OAUTH_PROVIDER_DATA[provider]

    if request.args.get('state') != login_session[provider]['state']:
        return make_json_response("Invalid state parameter", 401)

    code = request.args.get('code')
    token = get_oauth_token(provider_data, code)
    if token is None:
        logging.warning("Failed obtaining access token")
        return make_json_response("Cannot obtain oauth token", 500)

    retrieve_userinfo(token, provider, provider_data)
    flash("You are now logged in as {}".format(login_session['user']))

    return redirect(url_for('show_homepage'))


def create_user(login_session):
    user_provider = login_session['provider']
    user_email = login_session[user_provider].get('email')
    user_provider_id = login_session[user_provider]['id']
    if user_email is not None:
        gravatar_url = "https://www.gravatar.com/avatar/"
        gravatar_url += hashlib.md5(user_email.lower().encode('utf-8')).hexdigest() + "?"
        user = User(name=login_session['user'],
                    provider=user_provider,
                    provider_id=user_provider_id,
                    email=user_email,
                    picture=gravatar_url)
        login_session['avatar'] = gravatar_url
    else:
        user = User(name=login_session['user'],
                    provider=user_provider,
                    provider_id=user_provider_id)
    session.add(user)
    session.commit()
    user = session.query(User).filter_by(
        provider=user_provider,
        provider_id=login_session[user_provider]['id']).one()
    return user.id


def get_user_by_id(user_id):
    return session.query(User).filter_by(id=user_id).one()


def get_user_by_provider(login_session):
    try:
        provider = login_session['provider']
        user = session.query(User).filter_by(
            provider=provider,
            provider_id=login_session[provider]['id']).one()
        return user.id
    except:
        return None


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8888)
