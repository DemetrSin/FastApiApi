from fastapi import HTTPException
from sqlmodel import select
from films_db_models import Producer, Actor, Genre


def creation_routine_handler(lst, cls, session, db_film):
    """
       Routine handler for creating related entities and associating them with a film.

       This function iterates over a list of entity objects (e.g., producers or actors),
       checks if each entity already exists in the database, and associates it with the
       provided film. If the entity does not exist, it is created and associated with the film.

       Parameters:
       - lst (list): A list of entity objects to be created or associated with the film.
       - cls: The class type of the entity (e.g., Producer or Actor).
       - session (Session): The SQLModel session object for interacting with the database.
       - db_film: The film object with which the entities will be associated.

       Returns:
       - None

       Example Usage:
       creation_routine_handler(
           lst=producers,
           cls=Producer,
           session=session,
           db_film=db_film
       )
       """
    for entity in lst:
        db_entity = session.exec(select(cls).where(cls.name == entity.name)).first()
        if db_entity:
            db_entity.films.append(db_film)
        else:
            db_entity = cls.model_validate(entity)
            if isinstance(db_entity, Producer):
                db_film.producers.append(db_entity)
            elif isinstance(db_entity, Actor):
                db_film.actors.append(db_entity)
            elif isinstance(db_entity, Genre):
                db_film.genres.append(db_entity)


def if_not_routine_handler(obj, status_code, detail):
    if not obj:
        raise HTTPException(status_code=status_code, detail=detail)
    return obj


def session_routine_handler(obj, session):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
