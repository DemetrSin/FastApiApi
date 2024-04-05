from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
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


# class GenreModel(BaseModel):
#     id: int
#     genre_name: str
#
#     # class Config:
#     #     from_attributes = True
#
#
# class GenreCreateModel(GenreModel):
#     pass
#
#
# class ProducerModel(BaseModel):
#     id: int
#     full_name: str
#     films: List[Film] = []
#
#     class Config:
#         from_attributes = True
#
#
# class ProducerCreateModel(ProducerModel):
#     pass
#
#
# class ActorModel(BaseModel):
#     id: int
#     full_name: str
#     films: List[Film] = []
#
#     class Config:
#         from_attributes = True
#
#
# class ActorCreateModel(ActorModel):
#     pass
#
#
# class FilmModel(BaseModel):
#     id: int
#     film_name: str
#     release_date: Optional[str]
#     duration: Optional[int]
#     description: Optional[str]
#     rating: Optional[float]
#     producers: List[Producer] = []
#     actors: List[Actor] = []
#     genres: List[Genre] = []
#
#     class Config:
#         from_attributes = True
#         arbitrary_types_allowed = True
#
#
# class FilmCreateModel(FilmModel):
#     producers: Optional[List[ProducerCreateModel]] = []
#     actors: Optional[List[ActorCreateModel]] = []
#     genres: Optional[List[GenreCreateModel]] = []


class GenreBaseModel(BaseModel):
    genre_name: str


class GenreCreateModel(GenreBaseModel):
    pass


class GenreModel(GenreBaseModel):
    id: int

    class Config:
        orm_mode = True


class ProducerBaseModel(BaseModel):
    full_name: str


class ProducerCreateModel(ProducerBaseModel):
    pass


class ProducerModel(ProducerBaseModel):
    id: int
    films: List[Film] = []

    class Config:
        orm_mode = True


class ActorBaseModel(BaseModel):
    full_name: str


class ActorCreateModel(ActorBaseModel):
    pass


class ActorModel(ActorBaseModel):
    id: int
    films: List[Film] = []

    class Config:
        orm_mode = True


class FilmBaseModel(BaseModel):
    film_name: str
    release_date: Optional[str]
    duration: Optional[int]
    description: Optional[str]
    rating: Optional[float]


class FilmCreateModel(FilmBaseModel):
    producers: Optional[List[ProducerCreateModel]] = []
    actors: Optional[List[ActorCreateModel]] = []
    genres: Optional[List[GenreCreateModel]] = []


class FilmModel(FilmBaseModel):
    id: int
    producers: List[ProducerModel] = []
    actors: List[ActorModel] = []
    genres: List[GenreModel] = []

    class Config:
        orm_mode = True


@app.get('/films/{film_id}', response_model=FilmModel)
def get_film(film_id: int, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.id == film_id).first()
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


