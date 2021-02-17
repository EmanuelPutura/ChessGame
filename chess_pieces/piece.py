from abc import abstractmethod


class Piece:
    def __init__(self, parent, x, y, color):
        self._parent = parent
        self._x = x
        self._y = y
        self._color = color

    @abstractmethod
    def attempt_move(self, x, y):
        pass

    @abstractmethod
    def move(self, x, y):
        pass
