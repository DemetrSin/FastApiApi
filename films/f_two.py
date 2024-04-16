from sqlmodel import Field, Relationship, SQLModel


class FilmProducerAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
    producer_id: int | None = Field(default=None, primary_key=True, foreign_key='producer.id')


class FilmActorAssociation(SQLModel, table=True):
    film_id: int | None = Field(default=True, primary_key=True, foreign_key='film.id')
    actor_id: int | None = Field(default=True, primary_key=True, foreign_key='actor.id')


# class FilmGenreAssociation(SQLModel, table=True):
#     film_id: int | None = Field(default=None, primary_key=True, foreign_key='film.id')
#     genre_id: int | None = Field(default=None, primary_key=True, foreign_key='genre.id')


class FilmBase(SQLModel):
    name: str = Field(index=True)
    release_date: int
    duration: int
    description: str | None = Field(default='No description')
    rating: float


class Film(FilmBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    producers: list['Producer'] = Relationship(back_populates='films', link_model=FilmProducerAssociation)
    actors: list['Actor'] = Relationship(back_populates='films', link_model=FilmActorAssociation)


class FilmCreate(FilmBase):
    pass


class FilmPublic(FilmBase):
    id: int
    producers: list['ProducerPublic']
    actors: list['ActorPublic']


class ProducerBase(SQLModel):
    name: str = Field(index=True)


class Producer(ProducerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    films: list[Film] = Relationship(back_populates='producers', link_model=FilmProducerAssociation)


class ProducerCreate(ProducerBase):
    pass


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


class ActorPublic(ActorBase):
    id: int


class ActorPublicWithFilms(ActorBase):
    id: int
    films: list[FilmPublic]


