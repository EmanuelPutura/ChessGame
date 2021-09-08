from enum import Enum


class PieceColor(Enum):
    WHITE = 0
    BLACK = 1


class UserAccountConstants(Enum):
    SALT_BYTES_NUMBER = 32
    SHA256_ITERATIONS_NUMBER = 100000
