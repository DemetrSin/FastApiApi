import os

from passlib.hash import pbkdf2_sha256


def hash_password(password):
    salt = os.urandom(16)
    result = pbkdf2_sha256.hash(password, salt=salt)
    return result


def check_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)
