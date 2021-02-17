from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class Pawn(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)
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
            if self._parent[move_x][move_y] is not None:
                break
            if move_x == x and move_y == y:
                return True
        for move in self.__attack_moves:
            move_x, move_y = move[0] + self._x, move[1] + self._y
            if not self._validate_board_move(move_x, move_y):
                continue
            if move_x == x and move_y == y and self._parent[x][y] is not None and self._parent[x][y].color != self._color:
                return True
        return False

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        if len(self.__normal_moves) == 2:
            self.__normal_moves.pop()
        self._x = x
        self._y = y
