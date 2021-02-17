from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class Queen(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    # TODO: ? BishopType/RookType classes st no code reuse is involved below
    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if self._parent[x][y] is not None and self._parent[x][y].color == self._color:
            return False
        rook_type = bishop_type = False
        if abs(self._x - x) != abs(self._y - y):
            bishop_type = True
        if (self._x != x and self._y != y) or (self._x == x and self._y == y):
            rook_type = True
        if rook_type == bishop_type:
            return False
        if bishop_type:
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
        elif rook_type:
            if self._x != x:
                down = self._x < x
                if down:
                    for row in range(self._x + 1, x):
                        if self._parent[row][y] is not None or not self._validate_board_move(row, y):
                            return False
                else:
                    for row in range(x + 1, self._x):
                        if self._parent[row][y] is not None or not self._validate_board_move(row, y):
                            return False
            else:
                right = self._y < y
                if right:
                    for column in range(self._y + 1, y):
                        if self._parent[x][column] is not None or not self._validate_board_move(x, column):
                            return False
                else:
                    for column in range(y + 1, self._y):
                        if self._parent[x][column] is not None or not self._validate_board_move(x, column):
                            return False
            return True

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        self._x = x
        self._y = y
