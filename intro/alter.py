import random

from faker import Faker


def generate_random_users(num_users):
    faker = Faker()
    user_data = []
    for _ in range(num_users):
        name = faker.name()
        sex = random.choice((1, 2))
        age = random.randint(18, 80)
        score = random.randint(100, 2000)
        user_data.append((name, sex, age, score))
    return user_data