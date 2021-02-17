from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class King(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    # TODO: check for king entering a position where it could be captured
    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if self._parent[x][y] is not None and self._parent[x][y].color == self._color:
            return False
        if abs(self._x - x) > 1 or abs(self._y - y) > 1:
            return False
        return True

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('Cannot move to ({}, {}) cell.'.format(x, y))
        self._x = x
        self._y = y
