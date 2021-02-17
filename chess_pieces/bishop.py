from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class Bishop(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if abs(self._x - x) != abs(self._y - y):
            return False

        if self._parent[x][y] is not None and self._parent[x][y].color == self._color:
            return False

        down = self._x < x
        down = -1 if not down else down

        right = self._y < y
        right = -1 if not right else right

        for index in range(1, abs(self._x - x) + 1):
            row = self._x + index * down
            column = self._y + index * right
            if self._parent[row][column] is not None or not self._validate_board_move(row, column):
                return False
        return True

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        self._x = x
        self._y = y
