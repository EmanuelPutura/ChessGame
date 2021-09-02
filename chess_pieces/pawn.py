from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class Pawn(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)
        self.__made_move = False
        if self._color == PieceColor.WHITE:
            self.__normal_moves = [(-1, 0), (-2, 0)]
            self.__attack_moves = [(-1, -1), (-1, 1)]
        elif self._color == PieceColor.BLACK:
            self.__normal_moves = [(1, 0), (2, 0)]
            self.__attack_moves = [(1, -1), (1, 1)]

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        for move in self.__normal_moves:
            move_x, move_y = move[0] + self._x, move[1] + self._y
            if not self._validate_board_move(move_x, move_y):
                continue
            if self._parent[move_x, move_y] is not None:
                break
            if move_x == x and move_y == y:
                return True
        for move in self.__attack_moves:
            move_x, move_y = move[0] + self._x, move[1] + self._y
            if not self._validate_board_move(move_x, move_y):
                continue
            if move_x == x and move_y == y and self._parent[x, y] is not None and self._parent[x, y].color != self._color:
                return True
        return False

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        if (x, y) not in self.get_move_options():
            raise InvalidMoveError("InvalidMoveError: Piece '{}' cannot be moved to cell ({}, {}).".format(self.__class__.__name__, x, y))

        if len(self.__normal_moves) == 2:
            self.__normal_moves.pop()
        self._parent[x, y] = self
        self.__made_move = True

    def get_move_options(self, base_call=True):
        if base_call and super().get_move_options():
            return self.try_check_defense()
        options = []

        # normal moves
        move = self.__normal_moves[0]
        basic_move_condition = self._parent.validate_move(self._x + move[0], self._y + move[1]) and self._parent[self._x + move[0], self._y + move[1]] is None
        if basic_move_condition:
            coordinates = (self.x, self.y)
            old_piece = self._parent[self._x + move[0], self._y + move[1]]
            self._parent[self._x + move[0], self._y + move[1]] = self

            king = self._parent.get_king(self._color)
            if king.check_safe(king.x, king.y):
                options.append((coordinates[0] + move[0], coordinates[1] + move[1]))

            self._parent[coordinates[0] + move[0], coordinates[1] + move[1]] = old_piece
            self._parent[coordinates] = self

        if not self.__made_move and self._parent.validate_move(self._x + self.__normal_moves[1][0], self._y + self.__normal_moves[1][1]) \
                and self._parent[self._x + self.__normal_moves[1][0], self._y + self.__normal_moves[1][1]] is None and basic_move_condition:
            coordinates = (self.x, self.y)
            old_piece = self._parent[self._x + self.__normal_moves[1][0], self._y + self.__normal_moves[1][1]]
            self._parent[self._x + self.__normal_moves[1][0], self._y + self.__normal_moves[1][1]] = self

            king = self._parent.get_king(self._color)
            if king.check_safe(king.x, king.y):
                options.append((coordinates[0] + self.__normal_moves[1][0], coordinates[1] + self.__normal_moves[1][1]))

            self._parent[coordinates[0] + self.__normal_moves[1][0], coordinates[1] + self.__normal_moves[1][1]] = old_piece
            self._parent[coordinates] = self

        # attack moves
        for move in self.__attack_moves:
            if self._parent.validate_move(self._x + move[0], self._y + move[1]) and self._parent[self._x + move[0], self._y + move[1]] is not None \
                    and self._parent[self._x + move[0], self._y + move[1]].color != self._color:
                coordinates = (self.x, self.y)
                old_piece = self._parent[self._x + move[0], self._y + move[1]]
                self._parent[self._x + move[0], self._y + move[1]] = self

                king = self._parent.get_king(self._color)
                if king.check_safe(king.x, king.y):
                    options.append((coordinates[0] + move[0], coordinates[1] + move[1]))

                self._parent[coordinates] = self
                self._parent[coordinates[0] + move[0], coordinates[1] + move[1]] = old_piece
        return options
