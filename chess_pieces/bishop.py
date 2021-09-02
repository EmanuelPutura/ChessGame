from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class DiagonalTypeMovement(Piece):
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
            if self._parent[row, column] is not None:
                if row != x or column != y:
                    return False
            if not self._validate_board_move(row, column):
                return False
        return True

    def move(self, *args):
        pass

    def get_move_options(self, base_call=True):
        # NW, NE, SW, SE directions
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        options = []
        for direction in directions:
            x = self._x + direction[0]
            y = self._y + direction[1]

            while self._parent.validate_move(x, y) and (
                    self._parent[x, y] is None or self._parent[x, y].color != self._color):
                coordinates = (self.x, self.y)
                current_piece = self._parent[coordinates]
                old_piece = self._parent[x, y]
                self._parent[x, y] = current_piece

                king = self._parent.get_king(self._color)
                if king.check_safe(king.x, king.y):
                    options.append((x, y))

                self._parent[coordinates] = current_piece
                self._parent[x, y] = old_piece

                if self._parent[x, y] is not None and self._parent[x, y].color != self._color:
                    break
                x += direction[0]
                y += direction[1]

        return options


class Bishop(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if abs(self._x - x) != abs(self._y - y):
            return False

        if self._parent[x, y] is not None and self._parent[x, y].color == self._color:
            return False
        return DiagonalTypeMovement(self._parent, self._x, self._y, self._color).attempt_move(x, y)

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        if (x, y) not in self.get_move_options():
            raise InvalidMoveError("InvalidMoveError: Piece '{}' cannot be moved to cell ({}, {}).".format(self.__class__.__name__, x, y))

        self._parent[x, y] = self

    def get_move_options(self, base_call=True):
        if base_call and super().get_move_options():
            return self.try_check_defense()
        return DiagonalTypeMovement(self._parent, self._x, self._y, self._color).get_move_options()
