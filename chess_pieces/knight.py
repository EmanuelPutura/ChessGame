from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError


class Knight(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)
        self.__possible_moves = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if self._parent[x, y] is not None and self._parent[x, y].color == self._color:
            return False
        for move in self.__possible_moves:
            move_x, move_y = self._x + move[0], self._y + move[1]
            if not (x != move_x or y != move_y or not self._validate_board_move(move_x, move_y)):
                return True
            elif x == move_x and y == move_y:
                return True
        return False

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        if (x, y) not in self.get_move_options():
            raise InvalidMoveError("InvalidMoveError: Piece '{}' cannot be moved to cell ({}, {}).".format(self.__class__.__name__, x, y))

        self._parent[x, y] = self

    def get_move_options(self, base_call=True):
        if base_call and super().get_move_options():
            return self.try_check_defense()
        options = []

        for move in self.__possible_moves:
            if self._parent.validate_move(self._x + move[0], self._y + move[1]) and (self._parent[self._x + move[0], self._y + move[1]] is None or
                            self._parent[self._x + move[0], self._y + move[1]].color != self._color):
                coordinates = (self.x, self.y)
                old_piece = self._parent[self._x + move[0], self._y + move[1]]
                self._parent[self._x + move[0], self._y + move[1]] = self

                king = self._parent.get_king(self._color)
                if king.check_safe(king.x, king.y):
                    options.append((coordinates[0] + move[0], coordinates[1] + move[1]))

                self._parent[coordinates] = self
                self._parent[coordinates[0] + move[0], coordinates[1] + move[1]] = old_piece
        return options
