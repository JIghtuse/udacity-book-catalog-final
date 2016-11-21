from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from common import DATABASE_FILENAME


Base = declarative_base()


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description}


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)

    cover_url = Column(String(250))
    cover_url_attribution = Column(String(250))
    description = Column(String(250))
    author = Column(String(80))
    year = Column(Integer)
    buy_url = Column(String(250))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    def build_url(self):
        return "{}-{}".format(self.id, self.title.replace(' ', '-'))

    @property
    def serialize(self):
        return {'id': self.id,
                'title': self.title,
                'cover_url': self.cover_url,
                'cover_url_attribution': self.cover_url_attribution,
                'description': self.description,
                'author': self.author,
                'year': self.year,
                'buy_url': self.buy_url,
                'genre': self.genre.name,
                'user': self.user.name}


def main():
    # will create a new database
    engine = create_engine("sqlite:///" + DATABASE_FILENAME)

    # will add a tables in database representing Base derived classes
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
