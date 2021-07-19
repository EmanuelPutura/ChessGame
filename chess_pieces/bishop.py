from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class BishopTypeMovement(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        down = self._x < x
        down = -1 if not down else down

        right = self._y < y
        right = -1 if not right else right

        for index in range(1, abs(self._x - x) + 1):
            row = self._x + index * down
            column = self._y + index * right
            if self._parent[row][column] is not None:
                if row != x or column != y:
                    return False
            if not self._validate_board_move(row, column):
                return False
        return True

    def move(self, *args):
        pass

    def get_move_options(self):
        pass


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
        return BishopTypeMovement(self._parent, self._x, self._y, self._color).attempt_move(x, y)

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
        while self._parent.validate_move(x, y) and self._parent[x][y] is None:
            options.append((x, y))

        # N-E movement options
        x = self._x - 1
        y = self._y + 1
        while self._parent.validate_move(x, y) and self._parent[x][y] is None:
            options.append((x, y))

        # S-W movement options
        x = self._x + 1
        y = self._y - 1
        while self._parent.validate_move(x, y) and self._parent[x][y] is None:
            options.append((x, y))

        # S-E movement options
        x = self._x + 1
        y = self._y + 1
        while self._parent.validate_move(x, y) and self._parent[x][y] is None:
            options.append((x, y))

        return options
