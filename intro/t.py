from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_teams_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)

        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()


def create_heroes_teams():
    with Session(engine) as session:
        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print(team_wakaland.heroes)


def add_more_heroes():
    with Session(engine) as session:
        # Previous code here omitted 👈

        hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )
        team_preventers = session.get(Team, 1)
        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
        session.refresh(team_preventers)
        print(team_preventers.heroes)


def hero1():
    with Session(engine) as session:
        print('\n'*5)
        hero = session.exec(select(Hero).where(Hero.id == 1)).one()
        print(hero.team.headquarters)
        team_preventers = session.exec(select(Team).where(Team.name == 'Preventers')).one()
        hero.team = team_preventers
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print(hero)


def select_heroes():
    with Session(engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == 'Spider-Boy')).one()
        spiders_team = session.exec(select(Team).where(Team.id == hero_spider_boy.team_id)).first()
        print(spiders_team)
        print(hero_spider_boy.team)
        team_preventers = session.exec(select(Team).where(Team.name == 'Preventers')).one()
        print(team_preventers.heroes)
        print(hero_spider_boy.team.heroes)


def remove_heroes_team():
    with Session(engine) as session:
        spider_boy = session.exec(select(Hero).where(Hero.name == 'Spider-Boy')).one()
        spider_boy.team = None
        session.add(spider_boy)
        session.commit()
        session.refresh(spider_boy)
        print(spider_boy)


def main():
    create_db_and_tables()
    create_teams_heroes()
    create_heroes_teams()
    add_more_heroes()
    # hero1()
    select_heroes()
    remove_heroes_team()


if __name__ == "__main__":
    main()
