from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class Rook(Piece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def attempt_move(self, x, y):
        if (self._x != x and self._y != y) or (self._x == x and self._y == y):
            return False
        if self._x != x:
            down = self._x < x
            if down:
                for row in range(self._x + 1, x):
                    if self._parent[row][y] is not None:
                        return False
            else:
                for row in range(x + 1, self._x):
                    if self._parent[row][y] is not None:
                        return False
        else:
            right = self._y < y
            if right:
                for column in range(self._y + 1, y):
                    if self._parent[x][column] is not None:
                        return False
            else:
                for column in range(y + 1, self._y):
                    if self._parent[x][column] is not None:
                        return False
        return True

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('Cannot move to ({}, {}) cell.'.format(x, y))
        self._x = x
        self._y = y
