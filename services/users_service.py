from user_account.user import User


class UsersService:
    def __init__(self, users_repository):
        self.__users_repository = users_repository

    def insert(self, email, username, password):
        user = User(email, username, password)
        self.__users_repository.insert(user)
        