from abc import abstractmethod

from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class Piece:
    def __init__(self, parent, x, y, color):
        self._parent = parent
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, other):
        self._x = other

    @y.setter
    def y(self, other):
        self._y = other

    @property
    def color(self):
        return self._color

    @property
    def name(self):
        return self._color.name.lower() + " " + self.__class__.__name__.lower()

    def _validate_board_move(self, x, y):
        return not (x < 0 or y < 0 or x > 7 or y > 7)

    @abstractmethod
    def attempt_move(self, *args):
        pass

    @abstractmethod
    def move(self, x, y):
        pass

    def get_move_options(self, base_call=True):
        king = self._parent.get_king(self._color)
        return not king.check_safe(king.x, king.y)

    def try_check_defense(self):
        king = self._parent.get_king(self._color)
        dangerous_pieces = king.get_dangerous_pieces(king.x, king.y)
        options = []

        if self == king:
            for move in self.get_move_options(False):
                # simulate the move and check if the check danger would go away or not
                if king.check_safe(move[0], move[1]):
                    options.append(move)
            return options

        # the only way to escape from a double check is to move the king
        if len(dangerous_pieces) == 2:
            return options

        if king.check_safe(king.x, king.y):
            return options

        # first check if there is a dangerous knight or/and a dangerous pawn, which cannot be blocked by some other piece (they can only be captured)
        must_move_piece = None
        for piece in dangerous_pieces:
            if piece in ["Knight", "Pawn"]:
                piece = dangerous_pieces[piece][0]
                if (piece.x, piece.y) not in self.get_move_options(False):
                    return options  # then no possible option
                if must_move_piece is not None:
                    return options
                must_move_piece = piece

        if must_move_piece is not None:
            last_coordinates = (self._x, self._y)
            self._parent[must_move_piece.x, must_move_piece.y] = self

            ret_value = options
            if king.check_safe(king.x, king.y):
                ret_value = [(must_move_piece.x, must_move_piece.y)]

            self._parent[last_coordinates] = self
            self._parent[must_move_piece.x, must_move_piece.y] = must_move_piece
            return ret_value

        for piece in dangerous_pieces:
            direction = dangerous_pieces[piece][1]        # the direction from where the piece attacks
            dangerous_piece = dangerous_pieces[piece][0]  # the piece that produces the danger

            x = king.x + direction[0]
            y = king.y + direction[1]

            while True:
                if self._parent[x, y] is None:
                    if self.attempt_move(x, y):
                        options.append((x, y))
                elif self._parent[x, y] == dangerous_piece:
                    if self.attempt_move(x, y):
                        options.append((x, y))
                    break
                x = x + direction[0]
                y = y + direction[1]
        return options

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y and self._color == other.color

    def __repr__(self):
        piece_color = {PieceColor.WHITE: 'White', PieceColor.BLACK: 'Black'}
        return '{} {}: {}, {}'.format(piece_color[self._color], self.__class__.__name__, self._x, self._y)
