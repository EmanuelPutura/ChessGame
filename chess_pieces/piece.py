from abc import abstractmethod


class Piece:
    def __init__(self, parent, x, y, color):
        self._parent = parent
        self._x = x
        self._y = y
        self._color = color

    @property
    def color(self):
        return self._color

    def _validate_board_move(self, x, y):
        return not (x < 0 or y < 0 or x > 7 or y > 7)

    @abstractmethod
    def attempt_move(self, x, y):
        pass

    @abstractmethod
    def move(self, x, y):
        pass
