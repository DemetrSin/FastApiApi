import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from .api_routine_handler import ApiRoutineHandler
from .database import create_db_and_tables, engine
from .films_db_models import (Actor, ActorCreate, ActorPublic,
                              ActorPublicWithFilms, ActorUpdate, Film,
                              FilmCreate, FilmPublic, FilmPublicFull,
                              FilmUpdate, Genre, GenreCreate, GenrePublic,
                              GenrePublicWithFilms, GenreUpdate, Producer,
                              ProducerCreate, ProducerPublic,
                              ProducerPublicWithFilms, ProducerUpdate)

app = FastAPI()
handler = ApiRoutineHandler()


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
        handler.creation_routine_handler(
            lst=producers,
            cls=Producer,
            session=session,
            db_film=db_film
        )
        handler.creation_routine_handler(
            lst=actors,
            cls=Actor,
            session=session,
            db_film=db_film
        )
        handler.creation_routine_handler(
            lst=genres,
            cls=Genre,
            session=session,
            db_film=db_film
        )
        return handler.session_routine_handler(obj=db_film, session=session)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Film name must be unique")


@app.get('/films/{film_id}', response_model=FilmPublicFull)
def get_film(film_id, session: Session = Depends(get_session)):
    return handler.get_object_handler(cls=Film, obj_id=film_id, session=session)


@app.get('/films/', response_model=list[FilmPublic])
def get_films(
        *,
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    return handler.get_objects_handler(cls=Film, session=session, offset=offset, limit=limit)


@app.patch('/films/{film_id}/', response_model=FilmPublicFull)
def update_film(film_id: int, film: FilmUpdate, session: Session = Depends(get_session)):
    db_film = session.get(Film, film_id)
    if not db_film:
        raise HTTPException(status_code=404, detail='Film not Found')
    film_data = film.model_dump(exclude_unset=True)
    for key, value in film_data.items():
        if key == 'producers':
            db_film.producers = [Producer(**p) for p in value]
        elif key == 'actors':
            db_film.actors = [Actor(**a) for a in value]
        elif key == 'genres':
            db_film.genres = [Genre(**g) for g in value]
        else:
            setattr(db_film, key, value)
    return handler.session_routine_handler(obj=db_film, session=session)


@app.delete('/films/{film_id}')
def delete_films(film_id: int, session: Session = Depends(get_session)):
    return handler.deletion_handler(cls=Film, obj_id=film_id, session=session)


# PRODUCERS PART


@app.post('/producers/', response_model=ProducerPublic)
def create_producer(producer: ProducerCreate, session: Session = Depends(get_session)):
    db_producer = Producer.model_validate(producer)
    return handler.session_routine_handler(obj=db_producer, session=session)


@app.get('/producers/{producer_id}', response_model=ProducerPublicWithFilms)
def get_producer(*, session: Session = Depends(get_session), producer_id):
    return handler.get_object_handler(cls=Producer, obj_id=producer_id, session=session)


@app.get('/producers/', response_model=list[ProducerPublic])
def get_producers(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    return handler.get_objects_handler(cls=Producer, session=session, offset=offset, limit=limit)


@app.patch('/producers/{producer_id}', response_model=ProducerPublicWithFilms)
def update_producer(
        producer_id: int,
        producer: ProducerUpdate,
        session: Session = Depends(get_session)
):
    return handler.update_object_handler(obj=producer, cls=Producer, session=session, obj_id=producer_id)


@app.delete('/producers/{producer_id}')
def delete_producer(producer_id: int, session: Session = Depends(get_session)):
    return handler.deletion_handler(cls=Producer, obj_id=producer_id, session=session)


# ACTORS PART


@app.post('/actors/', response_model=ActorPublic)
def create_actor(actor: ActorCreate, session: Session = Depends(get_session)):
    db_actor = Actor.model_validate(actor)
    return handler.session_routine_handler(obj=db_actor, session=session)


@app.get('/actors/{actor_id}', response_model=ActorPublicWithFilms)
def get_actor(*, session: Session = Depends(get_session), actor_id):
    return handler.get_object_handler(cls=Actor, obj_id=actor_id, session=session)


@app.get('/actors/', response_model=list[ActorPublic])
def get_actors(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    return handler.get_objects_handler(cls=Actor, session=session, offset=offset, limit=limit)


@app.patch('/actors/{actor_id}', response_model=ActorPublicWithFilms)
def update_actor(
        actor_id: int,
        actor: ActorUpdate,
        session: Session = Depends(get_session)
):
    return handler.update_object_handler(obj=actor, cls=Actor, session=session, obj_id=actor_id)


@app.delete('/actors/{actor_id}')
def delete_actor(actor_id: int, session: Session = Depends(get_session)):
    return handler.deletion_handler(cls=Actor, obj_id=actor_id, session=session)


# GENRES PART


@app.post('/genres/', response_model=GenrePublic)
def create_genre(genre: GenreCreate, session: Session = Depends(get_session)):
    db_genre = Genre.model_validate(genre)
    return handler.session_routine_handler(obj=db_genre, session=session)


@app.get('/genres/{genre_id}/', response_model=GenrePublicWithFilms)
def get_genre(genre_id, session: Session = Depends(get_session)):
    return handler.get_object_handler(cls=Genre, obj_id=genre_id, session=session)


@app.get('/genres/', response_model=list[GenrePublic])
def get_genres(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(default=10, le=10)
):
    return handler.get_objects_handler(cls=Genre, session=session, offset=offset, limit=limit)


@app.patch('/genres/{genre_id}', response_model=GenrePublicWithFilms)
def update_genre(
        genre_id: int,
        genre: GenreUpdate,
        session: Session = Depends(get_session)
):
    return handler.update_object_handler(obj=genre, cls=Genre, session=session, obj_id=genre_id)


@app.delete('/genres/{genre_id}')
def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    return handler.deletion_handler(cls=Genre, obj_id=genre_id, session=session)


if __name__ == '__main__':
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Process is done')
