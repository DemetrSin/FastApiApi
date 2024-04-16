from sqlmodel import Field, Relationship, SQLModel


class FilmProducerAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    producer_id: int | None = Field(default=None, primary_key=True, foreign_key='producer.id')


class FilmActorAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    actor_id: int | None = Field(default=None, primary_key=True, foreign_key='actor.id')


class FilmGenreAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    genre_id: int | None = Field(default=None, primary_key=True, foreign_key='genre.id')


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
