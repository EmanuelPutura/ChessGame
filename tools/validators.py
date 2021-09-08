from errors.exceptions import PasswordsDoNotMatchError, InvalidAccountCredentialsError


class CredentialsValidator:
    @staticmethod
    def validate(email, username, password, repeated_password, users_service):
        if repeated_password != password:
            raise PasswordsDoNotMatchError("Passwords do not match!")
        if email == "":
            raise InvalidAccountCredentialsError("Invalid email address!")
        if username == "":
            raise InvalidAccountCredentialsError("Invalid username!")

        search_result = users_service.search(email, username)
        if search_result == 1:
            raise InvalidAccountCredentialsError("The email has already been used for another account!")
        if search_result == 2:
            raise InvalidAccountCredentialsError("The username has already been used for another account!")
