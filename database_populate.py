import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common import DATABASE_FILENAME
from database_setup import Base, Genre, Book, User


def parse_json_objects_data(filename, root):
    objects_data = []
    with open(filename) as objects_file:
        try:
            data = json.load(objects_file)
        except json.decoder.JSONDecodeError as e:
            logging.critical("Cannot get objects data: {}".format(e))
            return objects_data

        for object_data in data[root]:
            objects_data.append(object_data)

    return objects_data


def load_genres(filename):
    genres_data = parse_json_objects_data(filename, 'genres')
    for genre_data in genres_data:
        try:
            genre = Genre(**genre_data)
            yield genre
        except TypeError:
            logging.warning("Malformed genre data: {}".format(genre_data))
            continue


def load_books(filename, genres, session, importer):
    books_data = parse_json_objects_data(filename, 'books')
    for book_data in books_data:
        genre_name = book_data.get('genre')
        if genre_name is None:
            logging.warning("Missed genre for book {}".format(book_data))
            continue

        genre_query = session.query(Genre).filter_by(name=genre_name)
        if genre_query.count() == 0:
            logging.warning("No genre {} (book data: {})".format(genre_name,
                                                                 book_data))
            continue

        if book_data['user'] != importer.name:
            continue
        genre = genre_query.one()
        book_data['genre'] = genre
        book_data['genre_id'] = genre.id
        book_data['user'] = importer
        book_data['user_id'] = importer.id
        try:
            book = Book(**book_data)
            yield book
        except TypeError:
            logging.warning("Malformed book data: {}".format(book_data))
            continue


def main():
    engine = create_engine("sqlite:///" + DATABASE_FILENAME)

    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    importer = User(name="Importer",
                    email="nobody@example.com",
                    picture="https://www.gravatar.com/avatar/00000000000000000000000000000000",
                    provider="local",
                    provider_id="000")
    session.add(importer)
    session.commit()

    number_of_genres = session.query(Genre).count()
    if number_of_genres:
        # Do not insert data second time
        return None

    genres = load_genres("data/database_initial_genres.json")
    for genre in genres:
        session.add(genre)
    session.commit()

    books = load_books("data/database_initial_books.json",
                       genres, session, importer)
    for book in books:
        session.add(book)
    session.commit()


if __name__ == "__main__":
    main()
