from sqlmodel import Field, SQLModel, create_engine, Session, select
from tutorial import Hero, engine, create_db_and_tables


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


def create_data():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
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


def select_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero, Team).where(Hero.team_id == Team.id))
        for hero, team in heroes:
            print(f"Hero: {hero}\nTeam: {team}")


# JOIN


def select_heroes_join():
    with Session(engine) as session:
        heroes = session.exec(select(Hero, Team).join(Team))
        # OR
        heroes = session.exec(select(Hero, Team).join(Team, isouter=True))
        heroes = session.exec(select(Hero).join(Team, isouter=True).where(Team.name == "Preventers"))
        for hero in heroes:
            print(hero)

        heroes = session.exec(select(Hero, Team).join(Team, isouter=True).where(Team.name == "Preventers"))
        for hero, team in heroes:
            print(f"Hero: {hero}\nTeam: {team}")


# Update data connection


def update_connection():
    with Session(engine) as session:
        team_preventers = session.exec(select(Team).where(Team.name == 'Preventers')).first()
        spider_boy = session.exec(select(Hero).where(Hero.name == 'Spider-Boy')).first()
        # spider_boy = session.get(Hero, 3)
        spider_boy.team_id = team_preventers.id
        session.add(spider_boy)
        session.commit()


# Break data connection


def remove_connection():
    with Session(engine) as session:
        hero = session.get(Hero, 3)
        hero.team_id = None
        session.add(hero)
        session.commit()
        session.refresh(hero)
        print(hero)


def main():
    # create_db_and_tables()
    # create_data()
    # select_heroes()
    # select_heroes_join()
    # update_connection()
    remove_connection()


if __name__ == "__main__":
    main()

