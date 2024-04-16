import uvicorn

from films_db_models import (
    Film,
    FilmCreate,
    FilmPublic,
    FilmPublicFull,
    Producer,
    ProducerCreate,
    ProducerPublic,
    ProducerPublicWithFilms,
    Actor,
    ActorCreate,
    ActorPublic,
    ActorPublicWithFilms
)
from fastapi import FastAPI, Depends, Query, HTTPException
from database import create_db_and_tables, engine
from sqlmodel import Session, select

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.post('/films/', response_model=FilmPublicFull)
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


@app.get('/films/{film_id}', response_model=FilmPublicFull)
def get_film(film_id, session: Session = Depends(get_session)):
    db_film = session.get(Film, film_id)
    if not db_film:
        raise HTTPException(status_code=404, detail='Film not Found')
    return db_film


@app.get('/films/', response_model=list[FilmPublic])
def get_films(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_films = session.exec(select(Film).offset(offset).limit(limit)).all()
    if not db_films:
        raise HTTPException(status_code=404, detail='Films not Found')
    return db_films


def creation(lst, cls, session, db_film):
    for entity in lst:
        db_entity = session.exec(select(cls).where(cls.name == entity.name)).first()
        if db_entity:
            db_entity.films.append(db_film)
        else:
            db_entity = cls.model_validate(entity)
            if isinstance(db_entity, Producer):
                db_film.producers.append(db_entity)
            elif isinstance(db_entity, Actor):
                db_film.actors.append(db_entity)


@app.get('/producers/{producer_id}', response_model=ProducerPublicWithFilms)
def get_producer(*, session: Session = Depends(get_session), producer_id):
    db_producer = session.get(Producer, producer_id)
    if not db_producer:
        raise HTTPException(status_code=404, detail='Producer not Found')
    return db_producer


@app.get('/producers/', response_model=list[ProducerPublic])
def get_producers(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_producers = session.exec(select(Producer).offset(offset).limit(limit)).all()
    if not db_producers:
        raise HTTPException(status_code=404, detail='Producers not Found')

    return db_producers


@app.get('/actors/{actor_id}', response_model=ActorPublicWithFilms)
def get_actor(*, session: Session = Depends(get_session), actor_id):
    db_actor = session.get(Actor, actor_id)
    if not db_actor:
        raise HTTPException(status_code=404, detail='Actor not Found')
    return db_actor


@app.get('/actors/', response_model=list[ActorPublic])
def get_actors(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_actors = session.exec(select(Actor).offset(offset).limit(limit)).all()
    if not db_actors:
        raise HTTPException(status_code=404, detail='Actors not Found')
    return db_actors


if __name__ == '__main__':
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Process is done')
