from chess_pieces.bishop import BishopTypeMovement
from chess_pieces.piece import Piece
from chess_pieces.rook import RookTypeMovement
from errors.exceptions import InvalidMoveError


class Queen(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if self._parent[x][y] is not None and self._parent[x][y].color == self._color:
            return False
        rook_type = bishop_type = True
        if abs(self._x - x) != abs(self._y - y):
            bishop_type = False
        if (self._x != x and self._y != y) or (self._x == x and self._y == y):
            rook_type = False
        if rook_type == bishop_type:
            return False
        if bishop_type:
            return BishopTypeMovement(self._parent, self._x, self._y, self._color).attempt_move(x, y)
        elif rook_type:
            return RookTypeMovement(self._parent, self._x, self._y, self._color).attempt_move(x, y)

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        self._x = x
        self._y = y

    def get_move_options(self):
        options = []

        # N-W movement options
        x = self.x - 1
        y = self._y - 1

        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            x -= 1
            y -= 1

        # N-E movement options
        x = self._x - 1
        y = self._y + 1
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            x -= 1
            y += 1

        # S-W movement options
        x = self._x + 1
        y = self._y - 1
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            x += 1
            y -= 1

        # S-E movement options
        x = self._x + 1
        y = self._y + 1
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            x += 1
            y += 1

        # N movement options
        x = self._x - 1
        y = self._y
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            x -= 1

        # S movement options
        x = self._x + 1
        y = self._y
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            x += 1

        # W movement options
        x = self._x
        y = self._y - 1
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            y -= 1

        # E movement options
        x = self._x
        y = self._y + 1
        while self._parent.validate_move(x, y) and (self._parent[x][y] is None or self._parent[x][y].color != self._color):
            options.append((x, y))
            if self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                break
            y += 1

        return options
