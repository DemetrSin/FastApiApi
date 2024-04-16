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
from f_two import (
    FilmProducerAssociation,
    FilmBase,
    Film,
    FilmCreate,
    FilmPublic,
    Producer,
    ProducerCreate,
    ProducerPublic
)
from fastapi import FastAPI, Depends
from database import create_db_and_tables, engine
from sqlmodel import Session

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
        producers: list[ProducerCreate]
):
    db_film = Film.model_validate(film)
    for producer in producers:
        db_producer = Producer.model_validate(producer)
        db_film.producers.append(db_producer)
    session.add(db_film)
    session.commit()
    session.refresh(db_film)
    return db_film
