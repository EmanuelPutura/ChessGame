from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class RookTypeMovement(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if self._x != x:
            down = self._x < x
            if down:
                for row in range(self._x + 1, x):
                    if self._parent[row, y] is not None or not self._validate_board_move(row, y):
                        return False
            else:
                for row in range(x + 1, self._x):
                    if self._parent[row, y] is not None or not self._validate_board_move(row, y):
                        return False
        else:
            right = self._y < y
            if right:
                for column in range(self._y + 1, y):
                    if self._parent[x, column] is not None or not self._validate_board_move(x, column):
                        return False
            else:
                for column in range(y + 1, self._y):
                    if self._parent[x, column] is not None or not self._validate_board_move(x, column):
                        return False
        return True

    def move(self, *args):
        pass

    def get_move_options(self, base_call=True):
        # N, S, W, E directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        options = []
        for direction in directions:
            x = self._x + direction[0]
            y = self._y + direction[1]
            while self._parent.validate_move(x, y) and (
                    self._parent[x, y] is None or self._parent[x, y].color != self._color):
                options.append((x, y))
                if self._parent[x, y] is not None and self._parent[x, y].color != self._color:
                    break
                x += direction[0]
                y += direction[1]

        return options


class Rook(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if (self._x != x and self._y != y) or (self._x == x and self._y == y):
            return False
        if self._parent[x, y] is not None and self._parent[x, y].color == self._color:
            return False
        return RookTypeMovement(self._parent, self._x, self._y, self._color).attempt_move(x, y)

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        self._parent[x, y] = self

    def get_move_options(self, base_call=True):
        if base_call and super().get_move_options():
            return self.try_check_defense()
        return RookTypeMovement(self._parent, self._x, self._y, self._color).get_move_options()
