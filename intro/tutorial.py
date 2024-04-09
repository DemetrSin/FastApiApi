from sqlmodel import Field, Session, SQLModel, create_engine, select, or_, col


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)

        session.commit()


# SELECT - select(class)


# def select_heroes():
#     with Session(engine) as session:
#         statement = select(Hero)
#         results = session.execute(statement)
#         for result in results:
#             print(result)
#         print()
        # OR
        # print(results.all())  # returns a list

# OR

def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        print(heroes)


# WHERE - where(class.attr == value)


def select_heroes_where():
    with Session(engine) as session:
        heroes = session.exec(select(Hero).where(Hero.id == 2)).all()
        print(heroes[0])
        # OR
        statement_equal = session.exec(select(Hero).where(Hero.name == 'Deadpond').where(Hero.age == 48)).all()
        print(statement_equal)
        # OR
        statement_unequal = session.exec(select(Hero).where(Hero.age != 48))
        print(*[x for x in statement_unequal])
        # OR
        statement_more_or_equal = session.exec(select(Hero).where(Hero.age >= 35))
        print([x for x in statement_more_or_equal])
        # OR
        statement_multiple_where = session.exec(select(Hero).where(Hero.age >= 35).where(Hero.age <= 42)).all()
        print(statement_multiple_where)
        # OR
        statement_single_multiple_where_values = session.exec(select(Hero).where(Hero.age >= 35, Hero.age <= 42)).all()
        print(statement_single_multiple_where_values)
        # OR
        statement_where_or = session.exec(select(Hero).where(or_(Hero.age < 35, Hero.age > 90)))
        print(statement_where_or.__next__())
        print(next(statement_where_or))
        # OR
        statement_where_with_col = session.exec(select(Hero).where((col(Hero.age) < 35)))
        print([x for x in statement_where_with_col])


def main():
    # create_db_and_tables()
    # create_heroes()
    # select_heroes()
    select_heroes_where()


if __name__ == "__main__":
    main()
