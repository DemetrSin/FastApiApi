import os.path
import random
import time

from sqlmodel import Field, Session, SQLModel, create_engine, select, or_, col
from timer import outer
from faker import Faker


sqlite_file_name = "person.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)
engine2 = create_engine("sqlite:///person2.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    SQLModel.metadata.create_all(engine2)


def generate_random_users(num_users):
    faker = Faker()
    user_data = []
    for _ in range(num_users):
        name = faker.name()
        age = random.randint(18, 80)
        address = faker.address()
        user_data.append((name, age, address))
    return user_data


faker = Faker()


class PersonIndexed(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    address: str | None = Field(default=None, index=True)


class PersonNotIndexed(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int | None
    address: str | None

# This version is slower in every test.
# @outer(1, flag=True)
# def create_person():
#     with Session(engine) as session:
#         for _ in range(10000):
#             z = PersonNotIndexed(name=faker.name(), age=random.randint(18, 80), address=faker.address())
#             session.add(z)
#         session.commit()


@outer(1, flag=True)
def create_person_with_func():
    with Session(engine2) as session:
        for person in generate_random_users(10000):
            name, age, address = person
            pers = PersonNotIndexed(name=name, age=age, address=address)
            session.add(pers)
        session.commit()


def show_db_data():
    with Session(engine) as session:
        persons = session.exec(select(PersonIndexed)).all()
        print(persons)


def main():
    create_db_and_tables()
    create_person()
    create_person_with_func()
    # show_db_data()


if __name__ == '__main__':
    main()

