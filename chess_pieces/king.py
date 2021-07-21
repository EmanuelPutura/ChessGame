from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


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

        # now check for the case when the king enters a position where it could be captured

        # case1: check for 'pawn type' moves
        pawn_attacking_spots = []
        if self._color == PieceColor.WHITE:
            pawn_attacking_spots = [(-1, -1), (-1, 1)]
        elif self._color == PieceColor.BLACK:
            pawn_attacking_spots = [(1, -1), (1, 1)]

        for move in pawn_attacking_spots:
            if self._parent[x + move[0]][y + move[1]] is not None and self._parent[x + move[0]][y + move[1]].__class__.__name__ == "Pawn" and \
                    self._parent[x + move[0]][y + move[1]].color != self._color:
                return False

        # corresponding directions: NW, NE, SW, SE, N, S, W, E
        direction_options = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in direction_options:
            enemy_x = x + direction[0]
            enemy_y = y + direction[1]
            if self._parent.validate_move(enemy_x, enemy_y) and self._parent[enemy_x][enemy_y] is not None and \
                    (enemy_x != self._x or enemy_y != self._y) and self._parent[enemy_x][enemy_y].__class__.__name__ == "King":
                return False

        return True

    def move(self, x, y):
        if not self.attempt_move(x, y):
            raise InvalidMoveError('InvalidMoveError: Cannot move to ({}, {}) cell.'.format(x, y))
        self._x = x
        self._y = y

    def get_move_options(self):
        options = []

        # corresponding directions: NW, NE, SW, SE, N, S, W, E
        direction_options = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]

        for direction in direction_options:
            x = self._x + direction[0]
            y = self._y + direction[1]
            if self.attempt_move(x, y):
                options.append((x, y))

        return options
