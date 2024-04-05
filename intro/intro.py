from typing import Optional

from sqlmodel import Field, SQLModel, Session, create_engine, select


class HeroModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


hero_1 = HeroModel(name="Deadpond", secret_name="Dive Wilson")
hero_2 = HeroModel(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = HeroModel(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("sqlite:///database.db")


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()


with Session(engine) as session:
    statement = select(HeroModel).where(HeroModel.name == "Spider-Boy")
    hero = session.exec(statement).first()
    print(hero)


