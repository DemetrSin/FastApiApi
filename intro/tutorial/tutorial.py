from sqlmodel import Field, Session, SQLModel, col, create_engine, or_, select


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    team_id: int | None = Field(default=None, foreign_key='team.id')


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


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        results = session.execute(statement)
        for result in results:
            print(result)
        print()
        # OR
        print(results.all())  # returns a list
#         OR
        print(results.first())  # returns first row
        # print(results.one())  # returns ONLY ONE row OR Error


# OR


def select_heroes2():
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


# one(), first(), get()

def one_first_get():
    with Session(engine) as session:
        print(session.exec(select(Hero).where(Hero.id == 2)).first())
        print(session.exec(select(Hero).where(Hero.id == 9000)).first())  # None
        # OR
        print(session.exec(select(Hero).where(Hero.id == 2)).one())
        # print(session.exec(select(Hero).where(Hero.id == 9000)).one())  # Error
        print(session.get(Hero, 2))
        print(session.get(Hero, 9000))  # None


# LIMIT and OFFSET


def limit_and_offset():
    with Session(engine) as session:
        statement_limit = select(Hero).limit(3)
        statement_offset_limit = select(Hero).offset(3).limit(3)
        statement_mix = select(Hero).where(Hero.age >= 35).offset(1).limit(2)
        results = session.exec(statement_mix)
        heroes = results.all()
        print(heroes)
        # OR
        print(session.exec(select(Hero).where(Hero.age >= 35).offset(1).limit(1)).one())


# UPDATE

def update_heroes():
    with Session(engine) as session:
        hero1 = session.exec(select(Hero).where(Hero.name == 'Spider-Boy')).one()
        hero2 = session.exec(select(Hero).where(Hero.name == "Captain North America")).one()
        print(hero1)
        print(hero2)
        hero1.age = 18
        hero1.name = "Spider-Youngster"
        hero2.age = 35
        hero2.name = "Captain North America Except Canada"

        session.add(hero1)
        session.add(hero2)
        session.commit()
        session.refresh(hero1)
        session.refresh(hero2)
        print(hero1)
        print(hero2)


# DELETE


def delete_hero():
    with Session(engine) as session:
        hero = session.exec(select(Hero).where(Hero.name == 'Spider-Youngster')).first()
        session.delete(hero)
        session.commit()
        print('Deleted hero: ', hero)


def main():
    # create_db_and_tables()
    # create_heroes()
    # select_heroes()
    # select_heroes2()
    # select_heroes_where()
    # one_first_get()
    # limit_and_offset()
    # update_heroes()
    delete_hero()


if __name__ == "__main__":
    main()
