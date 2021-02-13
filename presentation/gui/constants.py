from enum import Enum


class Dimensions(Enum):
    MARGIN = 40
    WINDOW_LENGTH = 700
    WINDOW_HEIGHT = 700


class Colors(Enum):
    WHITE = (255, 255, 255)  # the color of the player that has the first move of the game

    GRAY = (170, 170, 170)

    BLACK1 = (0, 0, 0)
    BLACK2 = (20, 20, 20)
