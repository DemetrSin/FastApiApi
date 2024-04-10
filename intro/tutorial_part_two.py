from sqlmodel import Field, SQLModel, create_engine
from tutorial import Hero, engine, create_db_and_tables


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


# class HeroWithTeam(Hero):
#     team_id: int | None = Field(default=None, foreign_key='team.id')


def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()

