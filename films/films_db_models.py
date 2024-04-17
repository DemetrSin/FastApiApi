from sqlmodel import Field, Relationship, SQLModel


class FilmProducerAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    producer_id: int | None = Field(default=None, primary_key=True, foreign_key='producer.id')


class FilmActorAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=True, primary_key=True, foreign_key='film.id')
    actor_id: int | None = Field(default=True, primary_key=True, foreign_key='actor.id')


class FilmGenreAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    genre_id: int | None = Field(default=None, primary_key=True, foreign_key='genre.id')


class FilmBase(SQLModel):
    name: str = Field(index=True, unique=True)
    release_date: str
    duration: int
    description: str | None = Field(default='No description')
    rating: float


class Film(FilmBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    producers: list['Producer'] = Relationship(back_populates='films', link_model=FilmProducerAssociation)
    actors: list['Actor'] = Relationship(back_populates='films', link_model=FilmActorAssociation)
    genres: list['Genre'] = Relationship(back_populates='films', link_model=FilmGenreAssociation)


class FilmCreate(FilmBase):
    pass


class FilmUpdate(FilmBase):
    name: str | None = None
    release_date: str | None = None
    duration: int | None = None
    description: str | None = None
    rating: float | None = None
    producers: list['ProducerCreate'] | None = None
    actors: list['ActorCreate'] | None = None
    genres: list['GenreCreate'] | None = None


class FilmPublic(FilmBase):
    id: int


class FilmPublicFull(FilmBase):
    id: int
    producers: list['ProducerPublic']
    actors: list['ActorPublic']
    genres: list['GenrePublic']


class ProducerBase(SQLModel):
    name: str = Field(index=True)


class Producer(ProducerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    films: list[Film] = Relationship(back_populates='producers', link_model=FilmProducerAssociation)


class ProducerCreate(ProducerBase):
    pass


class ProducerUpdate(ProducerBase):
    name: str | None = None


class ProducerPublic(ProducerBase):
    id: int


class ProducerPublicWithFilms(ProducerBase):
    id: int
    films: list[Film]


class ActorBase(SQLModel):
    name: str = Field(index=True)


class Actor(ActorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    films: list[Film] = Relationship(back_populates='actors', link_model=FilmActorAssociation)


class ActorCreate(ActorBase):
    pass


class ActorUpdate(ActorBase):
    name: str | None = None


class ActorPublic(ActorBase):
    id: int


class ActorPublicWithFilms(ActorBase):
    id: int
    films: list[FilmPublic]


class GenreBase(SQLModel):
    name: str = Field(index=True)


class Genre(GenreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    films: list[Film] = Relationship(back_populates='genres', link_model=FilmGenreAssociation)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    name: str | None = None


class GenrePublic(GenreBase):
    id: int


class GenrePublicWithFilms(GenreBase):
    id: int
    films: list[FilmPublic]


