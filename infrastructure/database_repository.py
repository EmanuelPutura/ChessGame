import sqlite3

from errors.exceptions import RepositoryError
from infrastructure.memory_repository import MemoryRepository
from user_account.user import User


class DatabaseManager:
    @staticmethod
    def create_connection(database_path):
        connection = None
        try:
            connection = sqlite3.connect(database_path)
        except sqlite3.Error as error:
            raise RepositoryError("Database connection error occurred: '{}'\n".format(str(error)))
        return connection

    @staticmethod
    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except sqlite3.Error as error:
            raise RepositoryError("Database query execution error occurred: '{}'\n".format(str(error)))

    @staticmethod
    def execute_read_query(connection, query):
        cursor = connection.cursor()
        reading_result = None
        try:
            cursor.execute(query)
            reading_result = cursor.fetchall()
        except sqlite3.Error as error:
            raise RepositoryError("Database query execution error occurred: '{}'\n".format(str(error)))
        return reading_result


class UsersDatabaseManager(DatabaseManager):
    @staticmethod
    def get_database_line(user):
        print(r"('{}','{}','{}');".format(user.email, user.username, user.databaseKey))
        return r"('{}','{}','{}');".format(user.email, user.username, user.databaseKey)


class UsersDatabaseRepository(MemoryRepository):
    def __init__(self, database_path):
        super().__init__()
        self.__db_connection = UsersDatabaseManager.create_connection(database_path)
        self.__create_users_table()
        self.__load_data()

    def __create_users_table(self):
        query = "CREATE TABLE IF NOT EXISTS users (email TEXT NOT NULL, username TEXT NOT NULL, key TEXT NOT NULL);"
        UsersDatabaseManager.execute_query(self.__db_connection, query)

    def __load_data(self):
        self._entities = []
        select_users_query = 'SELECT * FROM users'
        users = DatabaseManager.execute_read_query(self.__db_connection, select_users_query)
        for user_line in users:
            user = User(user_line[0], user_line[1], user_line[2])
            super().insert(user)

    def insert(self, user):
        self.__load_data()
        super().insert(user)
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute("""INSERT INTO users (email, username, key) VALUES (?,?,?);""", (user.email, user.username, user.databaseKey))
            self.__db_connection.commit()
        except sqlite3.Error as error:
            raise RepositoryError("Database query execution error occurred: '{}'\n".format(str(error)))

    def remove(self, user):
        self.__load_data()
        super().remove(user)
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute("""DELETE FROM users where email = ? AND username = ?""", (user.email, user.username))
            self.__db_connection.commit()
        except sqlite3.Error as error:
            raise RepositoryError("Database query execution error occurred: '{}'\n".format(str(error)))

    def update(self, user, new_user):
        self.__load_data()
        super().update(user, new_user)
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute("""UPDATE users SET key = ?, username = ?, email = ? WHERE email = ? AND username = ?""", (new_user.databaseKey, new_user.username, new_user.email, user.email, user.username))
            self.__db_connection.commit()
        except sqlite3.Error as error:
            raise RepositoryError("Database query execution error occurred: '{}'\n".format(str(error)))
