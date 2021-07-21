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
        self._parent[x, y] = self

    def get_move_options(self):
        options = []

        for move in self.__possible_moves:
            if self._parent.validate_move(self._x + move[0], self._y + move[1]) and (self._parent[self._x + move[0], self._y + move[1]] is None or
                            self._parent[self._x + move[0], self._y + move[1]].color != self._color):
                options.append((self._x + move[0], self._y + move[1]))
        return options
