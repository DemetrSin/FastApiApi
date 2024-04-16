from sqlmodel import Field, Relationship, SQLModel


class FilmBase(SQLModel):
    name: str = Field(index=True)
    release_date: int
    duration: int
    description: str | None = Field(default='No description')
    rating: float


class Film(FilmBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    producer: list['Producer'] = Relationship(back_populates='films')


class FilmCreate(FilmBase):
    pass


class FilmPublic(FilmBase):
    id: int


class FilmUpdate(FilmBase):
    name: str | None = None
    release_date: int | None = None
    duration: int | None = None
    description: str | None = None
    rating: float | None = None


class ProducerBase(SQLModel):
    name: str = Field(index=True)


class Producer(ProducerBase):
    id: int | None = Field(default=None, primary_key=True)


class ProducerCreate(ProducerBase):
    pass


class ProducerPublic(ProducerBase):
    id: int


class ProducerUpdate(ProducerBase):
    name: str | None = None


class ActorBase(SQLModel):
    name: str = Field(index=True)


class Actor(ActorBase):
    id: int | None = Field(default=None, primary_key=True)


class ActorCreate(ActorBase):
    pass


class ActorPublic(ActorBase):
    id: int


class ActorUpdate(ActorBase):
    name: str | None = None


class GenreBase(SQLModel):
    name: str = Field(index=True)


class Genre(GenreBase):
    id: int | None = Field(default=None, primary_key=True)


class GenreCreate(GenreBase):
    pass


class GenrePublic(GenreBase):
    id: int


class GenreUpdate(ActorBase):
    name: str | None = None


class FilmPublicFull(FilmPublic):
    producers: list[ProducerPublic] = []
    actors: list[ActorPublic] = []
    genres: list[GenrePublic] = []


class ProducerPublicWithFilms(ProducerPublic):
    films: list[FilmPublic] = []


class ActorPublicWithFilms(ActorPublic):
    films: list[FilmPublic] = []


class GenrePublicWithFilms(GenrePublic):
    films: list[FilmPublic] = []




