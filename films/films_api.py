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
from fastapi import FastAPI, Depends, Query
from database import create_db_and_tables, engine
from sqlmodel import Session, select
from api_routine_handler import creation_routine_handler, if_not_routine_handler, session_routine_handler

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.post('/films/', response_model=FilmPublicFull)
def create_film(
        *,
        session: Session = Depends(get_session),
        film: FilmCreate,
        producers: list[ProducerCreate],
        actors: list[ActorCreate]
):
    db_film = Film.model_validate(film)
    creation_routine_handler(
        lst=producers,
        cls=Producer,
        session=session,
        db_obj=db_film
    )
    creation_routine_handler(
        lst=actors,
        cls=Actor,
        session=session,
        db_obj=db_film
    )
    session_routine_handler(obj=db_film, session=session)


@app.post('/actors/', response_model=ActorPublic)
def create_actor(actor: ActorCreate, session: Session = Depends(get_session)):
    db_actor = Actor.model_validate(actor)
    return session_routine_handler(obj=db_actor, session=session)


@app.get('/films/{film_id}', response_model=FilmPublicFull)
def get_film(film_id, session: Session = Depends(get_session)):
    db_film = session.get(Film, film_id)
    return if_not_routine_handler(obj=db_film, status_code=404, detail='Film not Found')


@app.get('/films/', response_model=list[FilmPublic])
def get_films(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_films = session.exec(select(Film).offset(offset).limit(limit)).all()
    return if_not_routine_handler(obj=db_films, status_code=404, detail='Films not Found')


@app.get('/producers/{producer_id}', response_model=ProducerPublicWithFilms)
def get_producer(*, session: Session = Depends(get_session), producer_id):
    db_producer = session.get(Producer, producer_id)
    return if_not_routine_handler(obj=db_producer, status_code=404, detail='Producer not Found')


@app.get('/producers/', response_model=list[ProducerPublic])
def get_producers(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_producers = session.exec(select(Producer).offset(offset).limit(limit)).all()
    return if_not_routine_handler(obj=db_producers, status_code=404, detail='Producers not Found')


@app.get('/actors/{actor_id}', response_model=ActorPublicWithFilms)
def get_actor(*, session: Session = Depends(get_session), actor_id):
    db_actor = session.get(Actor, actor_id)
    return if_not_routine_handler(obj=db_actor, status_code=404, detail='Actor not Found')


@app.get('/actors/', response_model=list[ActorPublic])
def get_actors(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_actors = session.exec(select(Actor).offset(offset).limit(limit)).all()
    return if_not_routine_handler(obj=db_actors, status_code=404, detail='Actors not Found')


if __name__ == '__main__':
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Process is done')
