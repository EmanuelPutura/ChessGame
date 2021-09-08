class UserInputError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class IsCheckError(InvalidMoveError):
    pass


class InvalidPieceError(Exception):
    pass


class RepositoryError(Exception):
    pass


class PasswordsDoNotMatchError(Exception):
    pass


class InvalidAccountCredentialsError(Exception):
    pass


class InvalidVerificationCodeError(Exception):
    pass


class LoginError(Exception):
    pass
