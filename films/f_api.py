# from f import (
#     FilmBase,
#     Film,
#     FilmCreate,
#     FilmPublic,
#     FilmUpdate,
#     ProducerBase,
#     Producer,
#     ProducerCreate,
#     ProducerPublic,
#     ProducerUpdate,
#     ActorBase,
#     Actor,
#     ActorCreate,
#     ActorPublic,
#     ActorUpdate,
#     GenreBase,
#     Genre,
#     GenreCreate,
#     GenrePublic,
#     GenreUpdate,
#     FilmPublicFull,
#     ProducerPublicWithFilms,
#     ActorPublicWithFilms,
#     GenrePublicWithFilms,
# )
import sys

import uvicorn

from f_two import (
    FilmProducerAssociation,
    FilmBase,
    Film,
    FilmCreate,
    FilmPublic,
    Producer,
    ProducerCreate,
    ProducerPublic,
    ProducerPublicWithFilms,
    Actor,
    ActorCreate,
    ActorPublic,
    ActorPublicWithFilms
)
from fastapi import FastAPI, Depends
from database import create_db_and_tables, engine
from sqlmodel import Session, select

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.post('/films/', response_model=FilmPublic)
def post_film(
        *,
        session: Session = Depends(get_session),
        film: FilmCreate,
        producers: list[ProducerCreate],
        actors: list[ActorCreate]
):
    db_film = Film.model_validate(film)
    # for producer in producers:
    #     db_producer = session.exec(select(Producer).where(Producer.name == producer.name)).first()
    #     if db_producer:
    #         db_producer.films.append(db_film)
    #     else:
    #         db_producer = Producer.model_validate(producer)
    #         db_film.producers.append(db_producer)
    creation(lst=producers, cls=Producer, session=session, db_film=db_film)
    creation(lst=actors, cls=Actor, session=session, db_film=db_film)
    session.add(db_film)
    session.commit()
    session.refresh(db_film)
    return db_film


def creation(lst, cls, session, db_film):
    for entity in lst:
        db_entity = session.exec(select(cls).where(cls.name == entity.name)).first()
        if db_entity:
            db_entity.films.append(db_film)
        else:
            db_entity = cls.model_validate(entity)
            db_film.producers.append(db_entity)


@app.get('/producers/{producer_id}', response_model=ProducerPublicWithFilms)
def get_producer(*, session: Session = Depends(get_session), producer_id):
    db_producer = session.get(Producer, producer_id)
    return db_producer


if __name__ == '__main__':
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Process is done')
