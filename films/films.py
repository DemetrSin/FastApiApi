from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from films_db_models import Film, Producer, Actor, Genre, FilmProducerAssociation, FilmActorAssociation, FilmGenreAssociation, Base


app = FastAPI()


SQLALCHEMY_DATABASE_URL = "sqlite:///./films.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class GenreModel(BaseModel):
    id: int
    genre_name: str

    class Config:
        orm_mode = True


class GenreCreateModel(GenreModel):
    pass


class ProducerModel(BaseModel):
    id: int
    full_name: str
    films: List[Film] = []

    class Config:
        orm_mode = True


class ProducerCreateModel(ProducerModel):
    pass


class ActorModel(BaseModel):
    id: int
    full_name: str
    films: List[Film] = []

    class Config:
        orm_mode = True


class ActorCreateModel(ActorModel):
    pass


class FilmModel(BaseModel):
    id: int
    film_name: str
    release_date: Optional[str]
    duration: Optional[int]
    description: Optional[str]
    rating: Optional[float]
    producers: List[Producer] = []
    actors: List[Actor] = []
    genres: List[Genre] = []

    class Config:
        orm_mode = True


class FilmCreateModel(FilmModel):
    producers: Optional[List[ProducerCreateModel]] = []
    actors: Optional[List[ActorCreateModel]] = []
    genres: Optional[List[GenreCreateModel]] = []
