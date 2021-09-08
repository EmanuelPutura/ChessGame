from errors.exceptions import PasswordsDoNotMatchError, InvalidAccountCredentialsError


class CredentialsValidator:
    @staticmethod
    def validate(email, username, password, repeated_password):
        if repeated_password != password:
            raise PasswordsDoNotMatchError("Passwords do not match!")
        if email == "":
            raise InvalidAccountCredentialsError("Invalid email address!")
        if username == "":
            raise InvalidAccountCredentialsError("Invalid username!")
