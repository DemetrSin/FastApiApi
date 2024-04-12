from fastapi import FastAPI
from sqlmodel import Session

from database import create_db_and_tables, engine
from films_db_models import Film, Producer, Genre, Actor

app = FastAPI()


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


@app.post('/films/', response_model=Film)
def create_films(film: Film, producers: list[Producer], actors: list[Actor], genres: list[Genre]):
    with Session(engine) as session:
        session.add(film)

        for producer in producers:
            session.add(producer)

        for actor in actors:
            session.add(actor)

        for genre in genres:
            session.add(genre)

        session.commit()

        session.refresh(film)

        return film
