from abc import abstractmethod

from tools.constants import PieceColor


class Piece:
    def __init__(self, parent, x, y, color):
        self._parent = parent
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return self.__class__.__name__

    def _validate_board_move(self, x, y):
        return not (x < 0 or y < 0 or x > 7 or y > 7)

    @abstractmethod
    def attempt_move(self, *args):
        pass

    @abstractmethod
    def move(self, *args):
        pass

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._color == other.color

    def __repr__(self):
        piece_color = {PieceColor.WHITE: 'White', PieceColor.BLACK: 'Black'}
        return '{} {}: {}, {}'.format(piece_color[self._color], self.__class__.__name__, self._x, self._y)
