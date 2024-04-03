from typing import List

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

app = FastAPI()

Base = declarative_base()


class Film(Base):
    __tablename__ = 'Films'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    release_date = Column(Date)
    duration = Column(Integer)
    description = Column(String)
    rating = Column(Float)
    producers = relationship('Producer', secondary='film_producer_association')
    actors = relationship("Actor", secondary="film_actor_association", back_populates="films")
    genres = relationship("Genre", secondary="film_genre_association", back_populates="films")


class Producer(Base):
    __tablename__ = 'Producers'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String)
    films = relationship("Film", secondary="film_producer_association", back_populates="producers")


class Actor(Base):
    __tablename__ = 'Actors'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String)
    films = relationship("Film", secondary="film_actor_association")


class Genre(Base):
    __tablename__ = 'Genres'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    films = relationship("Film", secondary="film_genre_association")


class FilmProducerAssociation(Base):
    __tablename__ = 'film_producer_association'
    film_id = Column(Integer, ForeignKey('Films.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('Producers.id'), primary_key=True)


class FilmActorAssociation(Base):
    __tablename__ = 'film_actor_association'
    film_id = Column(Integer, ForeignKey('Films.id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('Actors.id'), primary_key=True)


class FilmGenreAssociation(Base):
    __tablename__ = 'film_genre_association'
    film_id = Column(Integer, ForeignKey('Films.id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('Genres.id'), primary_key=True)


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


