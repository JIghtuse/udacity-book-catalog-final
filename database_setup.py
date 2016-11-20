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

    def build_url(self):
        return "{}-{}".format(self.id, self.title.replace(' ', '-'))


def main():
    # will create a new database
    engine = create_engine("sqlite:///" + DATABASE_FILENAME)

    # will add a tables in database representing Base derived classes
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
