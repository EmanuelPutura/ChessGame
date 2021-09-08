from tools.constants import UserAccountConstants


class User:
    def __init__(self, email, username, key):
        self.__email = email
        self.__username = username
        self.__salt = key[:UserAccountConstants.SALT_BYTES_NUMBER.value]
        self.__key = key[UserAccountConstants.SALT_BYTES_NUMBER.value:]

    @property
    def email(self):
        return self.__email

    @property
    def username(self):
        return self.__username

    @property
    def key(self):
        return self.__key

    @property
    def databaseKey(self):
        return self.__salt + self.__key

    @key.setter
    def key(self, other):
        self.__key = other

    def __str__(self):
        return 'Email: {}, Username: {}, Salt: {}, Key: {}'.format(self.__email, self.__username, self.__salt, self.__key)

    def __eq__(self, other):
        return self.__email == other.email or self.__username == other.username
