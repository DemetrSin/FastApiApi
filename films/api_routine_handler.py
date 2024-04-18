from fastapi import HTTPException
from sqlmodel import select

from films_db_models import Actor, Genre, Producer


class ApiRoutineHandler:
    @staticmethod
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

    @staticmethod
    def if_not(*, obj, cls):
        if not obj:
            detail = f"{cls.__name__} not Found"
            raise HTTPException(status_code=404, detail=detail)

    def get_object_handler(self, *, cls, obj_id, session):
        db_obj = session.get(cls, obj_id)
        self.if_not(obj=db_obj, cls=cls)
        return db_obj

    def get_objects_handler(self, *, cls, session, offset, limit):
        db_objects = session.exec(select(cls).offset(offset).limit(limit)).all()
        self.if_not(obj=db_objects, cls=cls)
        return db_objects

    def update_object_handler(self, *, obj, cls, session, obj_id):
        db_obj = session.get(cls, obj_id)
        self.if_not(obj=db_obj, cls=cls)
        obj_data = obj.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        return self.session_routine_handler(obj=db_obj, session=session)

    @staticmethod
    def session_routine_handler(obj, session):
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def deletion_handler(self, *, cls, obj_id, session,):
        db_obj = session.get(cls, obj_id)
        self.if_not(obj=db_obj, cls=cls)
        session.delete(db_obj)
        session.commit()
        return {'ok': 'Successful deletion'}
