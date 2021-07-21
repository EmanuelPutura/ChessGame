from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class King(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if self._parent[x][y] is not None and self._parent[x][y].color == self._color:
            return False
        if abs(self._x - x) > 1 or abs(self._y - y) > 1:
            return False

        # now check for the case when the king enters a position where it could be captured
        return self.__checkMoveForCaptureDanger(x, y)

    def __checkMoveForCaptureDanger(self, x, y):
        directions = []
        if self._color == PieceColor.WHITE:
            directions = [(-1, -1), (-1, 1)]
        elif self._color == PieceColor.BLACK:
            directions = [(1, -1), (1, 1)]

        # in order of the direction: NW, NE, SW, SE, N, S, W, E and then the knight directions
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        pieces_to_be_checked = [["Pawn"], ["King"], ["Knight"], ["Bishop", "Queen"], ["Rook", "Queen"]]
        directions_limit = [2, 10, len(directions) - 1, len(directions) + 3]  # at index 2 change to 'king type' and at index 10 change to 'knight type' movement

        loop_index = 0
        limit_index = 0  # index in directions_limit and pieces_to_be_checked lists

        for direction in directions + directions[2:10]:
            if limit_index < 4 and loop_index == directions_limit[limit_index]:
                limit_index += 1

            enemy_x = x + direction[0]
            enemy_y = y + direction[1]

            if loop_index > 17:
                while self._parent.validate_move(enemy_x, enemy_y) and self._parent[enemy_x][enemy_y] is None:
                    enemy_x += direction[0]
                    enemy_y += direction[1]

            if self._parent.validate_move(enemy_x, enemy_y) and self._parent[enemy_x][enemy_y] is not None and \
                    self._parent[enemy_x][enemy_y].__class__.__name__ in pieces_to_be_checked[limit_index] and self._parent[enemy_x][enemy_y].color != self._color:
                return False
            loop_index += 1

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
