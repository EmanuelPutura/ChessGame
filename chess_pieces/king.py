from chess_pieces.piece import Piece
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class King(Piece):
    def __init__(self, parent, x, y, color):
        super().__init__(parent, x, y, color)

    def attempt_move(self, x, y):
        if not self._validate_board_move(x, y):
            return False
        if self._parent[x, y] is not None and self._parent[x, y].color == self._color:
            return False
        if abs(self._x - x) > 1 or abs(self._y - y) > 1:
            return False
        return self.check_safe(x, y)  # now check for the case when the king enters a position where it could be captured

    def check_safe(self, x, y):
        return True if self.get_dangerous_pieces(x, y) == {} else False

    def get_dangerous_pieces(self, x, y):
        dangerous_pieces = {}
        directions = []

        if self._color == PieceColor.WHITE:
            directions = [(-1, -1), (-1, 1)]
        elif self._color == PieceColor.BLACK:
            directions = [(1, -1), (1, 1)]

        # in order of the direction: NW, NE, SW, SE, N, S, W, E and then the knight directions
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -2), (-2, -1),
                       (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        pieces_to_be_checked = [["Pawn"], ["King"], ["Knight"], ["Bishop", "Queen"], ["Rook", "Queen"]]
        directions_limit = [2, 10, 18, 22]  # at index 2 change to 'king type' and at index 10 change to 'knight type' movement (and so on)

        loop_index = 0
        limit_index = 0  # index in directions_limit and pieces_to_be_checked lists

        for direction in directions + directions[2:10]:
            if limit_index < 4 and loop_index == directions_limit[limit_index]:
                limit_index += 1

            enemy_x = x + direction[0]
            enemy_y = y + direction[1]

            if 17 < loop_index:
                while self._parent.validate_move(enemy_x, enemy_y) and self._parent[enemy_x, enemy_y] is None:
                    enemy_x += direction[0]
                    enemy_y += direction[1]
            if self._parent.validate_move(enemy_x, enemy_y) and self._parent[enemy_x, enemy_y] is not None and \
                    self._parent[enemy_x, enemy_y].__class__.__name__ in pieces_to_be_checked[limit_index] and \
                    self._parent[enemy_x, enemy_y].color != self._color:
                dangerous_pieces[self._parent[enemy_x, enemy_y].__class__.__name__ + str(enemy_x) + str(enemy_y)] = (self._parent[enemy_x, enemy_y], direction)
            loop_index += 1
        return dangerous_pieces

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

        # corresponding directions: NW, NE, SW, SE, N, S, W, E
        direction_options = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]

        for direction in direction_options:
            x = self._x + direction[0]
            y = self._y + direction[1]
            if self.attempt_move(x, y):
                options.append((x, y))

        return options
