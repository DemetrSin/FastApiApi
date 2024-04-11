from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class FilmProducerAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    producer_id: int | None = Field(default=None, primary_key=True, foreign_key='producer.id')


class FilmActorAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    producer_id: int | None = Field(default=None, primary_key=True, foreign_key='actor.id')


class FilmGenreAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    producer_id: int | None = Field(default=None, primary_key=True, foreign_key='genre.id')


class Film(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    release_date: int
    duration: int
    description: str | None = Field(default='No description')
    rating: float
    producers: list['Producer'] = Relationship(back_populates='films', link_model=FilmProducerAssociation)
    actors: list['Actor'] = Relationship(back_populates='films', link_model=FilmActorAssociation)
    genres: list['Genre'] = Relationship(back_populates='films', link_model=FilmGenreAssociation)


class Producer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    films: list[Film] = Relationship(back_populates='producers', link_model=FilmProducerAssociation)


class Actor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    films: list[Film] = Relationship(back_populates='actors', link_model=FilmActorAssociation)


class Genre(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    films: list[Film] = Relationship(back_populates='genres', link_model=FilmGenreAssociation)


sqlite_file_name = "films.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_data():
    with Session(engine) as session:
        dune = Film(
            name='Dune',
            release_date=2021,
            duration=149,
            rating=4.5,
        )
        deni_vilnev = Producer(name='Deni Vilnev', films=[dune])
        ostin_batler = Actor(name='Ostin Batler', films=[dune])
        timoti_shalame = Actor(name='Timoti Shalame', films=[dune])
        adventure = Genre(name='Adventure', films=[dune])
        session.add_all((dune, deni_vilnev, ostin_batler, timoti_shalame, adventure))
        # session.commit()
        dune_from_db = session.exec(select(Film).where(Film.name == 'Dune')).one()
        print(dune_from_db)
        print(dune_from_db.producers)
        print(dune_from_db.actors)
        print(dune_from_db.genres)
        actor = session.get(Actor, 1)
        print(actor)


def main():
    create_db_and_tables()
    create_data()


if __name__ == "__main__":
    main()







