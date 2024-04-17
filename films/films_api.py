import uvicorn

from films_db_models import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmPublic,
    FilmPublicFull,
    Producer,
    ProducerCreate,
    ProducerUpdate,
    ProducerPublic,
    ProducerPublicWithFilms,
    Actor,
    ActorCreate,
    ActorUpdate,
    ActorPublic,
    ActorPublicWithFilms,
    Genre,
    GenreCreate,
    GenreUpdate,
    GenrePublic,
    GenrePublicWithFilms
)
from fastapi import FastAPI, Depends, Query, HTTPException
from database import create_db_and_tables, engine
from sqlmodel import Session, select
from api_routine_handler import creation_routine_handler, if_not_routine_handler, session_routine_handler
from sqlalchemy.exc import IntegrityError

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


# FILMS PART


@app.post('/films/', response_model=FilmPublicFull)
def create_film(
        *,
        session: Session = Depends(get_session),
        film: FilmCreate,
        producers: list[ProducerCreate],
        actors: list[ActorCreate],
        genres: list[GenreCreate]
):
    try:
        db_film = Film.model_validate(film)
        creation_routine_handler(
            lst=producers,
            cls=Producer,
            session=session,
            db_film=db_film
        )
        creation_routine_handler(
            lst=actors,
            cls=Actor,
            session=session,
            db_film=db_film
        )
        creation_routine_handler(
            lst=genres,
            cls=Genre,
            session=session,
            db_film=db_film
        )
        return session_routine_handler(obj=db_film, session=session)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Film name must be unique")


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


@app.patch('/films/{film_id}/', response_model=FilmPublicFull)
def update_film(film_id: int, film: FilmUpdate, session: Session = Depends(get_session)):
    db_film = session.get(Film, film_id)
    if not db_film:
        raise HTTPException(status_code=404, detail='Film not Found')
    film_data = film.model_dump(exclude_unset=True)
    print('\n'*5)
    print(film_data)
    print('\n'*5)
    for key, value in film_data.items():
        if key == 'producers':
            db_film.producers = [Producer(**p) for p in value]
        elif key == 'actors':
            db_film.actors = [Actor(**a) for a in value]
        elif key == 'genres':
            db_film.genres = [Genre(**g) for g in value]
        else:
            setattr(db_film, key, value)
    return session_routine_handler(obj=db_film, session=session)


# PRODUCERS PART


@app.post('/producers/', response_model=ProducerPublic)
def create_producer(producer: ProducerCreate, session: Session = Depends(get_session)):
    db_producer = Producer.model_validate(producer)
    return session_routine_handler(obj=db_producer, session=session)


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


@app.patch('/producers/{producer_id}', response_model=ProducerPublicWithFilms)
def update_producer(
        producer_id: int,
        producer: ProducerUpdate,
        session: Session = Depends(get_session)
):
    db_producer = session.get(Producer, producer_id)
    if not db_producer:
        raise HTTPException(status_code=404, detail='Producer not Found')
    producer_data = producer.model_dump(exclude_unset=True)
    for key, value in producer_data.items():
        setattr(db_producer, key, value)
    return session_routine_handler(obj=db_producer, session=session)


# ACTORS PART


@app.post('/actors/', response_model=ActorPublic)
def create_actor(actor: ActorCreate, session: Session = Depends(get_session)):
    db_actor = Actor.model_validate(actor)
    return session_routine_handler(obj=db_actor, session=session)


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


@app.patch('/actors/{actor_id}', response_model=ActorPublicWithFilms)
def update_actor(
        actor_id: int,
        actor: ActorUpdate,
        session: Session = Depends(get_session)
):
    db_actor = session.get(Actor, actor_id)
    if not db_actor:
        raise HTTPException(status_code=404, detail='Actor not Found')
    actor_data = actor.model_dump(exclude_unset=True)
    for key, value in actor_data.items():
        setattr(db_actor, key, value)
    return session_routine_handler(obj=db_actor, session=session)


# GENRES PART


@app.post('/genres/', response_model=GenrePublic)
def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    db_genre = Genre.model_validate(genre)
    return session_routine_handler(obj=db_genre, session=session)


@app.get('/genres/{genre_id}/', response_model=GenrePublicWithFilms)
def get_genre(genre_id, session: Session = Depends(get_session)):
    db_genre = session.get(Genre, genre_id)
    return if_not_routine_handler(obj=db_genre, status_code=404, detail='Genre not Found')


@app.get('/genres/', response_model=list[GenrePublic])
def get_genres(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    db_genres = session.exec(select(Genre).offset(offset).limit(limit)).all()
    return if_not_routine_handler(obj=db_genres, status_code=404, detail='Genres not Found')


@app.patch('/genres/{genre_id}', response_model=GenrePublicWithFilms)
def update_genre(
        genre_id: int,
        genre: GenreUpdate,
        session: Session = Depends(get_session)
):
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail='Genre not Found')
    genre_data = genre.model_dump(exclude_unset=True)
    for key, value in genre_data.items():
        setattr(db_genre, key, value)
    return session_routine_handler(obj=db_genre, session=session)


if __name__ == '__main__':
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Process is done')
