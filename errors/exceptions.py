class UserInputError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class IsCheckError(InvalidMoveError):
    pass
