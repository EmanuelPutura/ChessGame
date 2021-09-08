from enum import Enum


class PieceColor(Enum):
    WHITE = 0
    BLACK = 1


class UserAccountConstants(Enum):
    SALT_BYTES_NUMBER = 32
    SHA256_ITERATIONS_NUMBER = 100000
    VERIFICATION_CODE_LOW = 100000
    VERIFICATION_CODE_HIGH = 999999
    EMAIL_SENDER = "quesschessgame@gmail.com"
    CONFIRMATION_MESSAGE = """\
        Subject: Quess account confirmation

        Welcome to the Quess community, """
    DEFAULT_ACCOUNT_IMAGE_PATH = r"\\assets\avatar.png"
