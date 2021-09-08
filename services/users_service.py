import hashlib
import os

from tools.constants import UserAccountConstants
from user_account.user import User


class UsersService:
    def __init__(self, users_repository):
        self.__users_repository = users_repository

    def insert(self, email, username, password):
        salt = os.urandom(32)  # returns a string which represents random bytes suitable for cryptographic use
        key = hashlib.pbkdf2_hmac(
            'sha256',  # the hash digest algorithm for HMAC
            password.encode('utf-8'),  # convert the password to bytes
            salt,  # the salt - makes the search space larger in case of attacks
            UserAccountConstants.SHA256_ITERATIONS_NUMBER.value  # it is recommended to use at least 100,000 iterations of SHA-256 - for more computational work, which helps avoiding attacks
            )

        storage = salt + key
        user = User(email, username, storage)
        self.__users_repository.insert(user)

    def search(self, email, username):
        for user in self.__users_repository.entities:
            if user.email == email:
                return 1
            if user.username == username:
                return 2
        return 0
