from texttable import Texttable

from chess_pieces.bishop import Bishop
from chess_pieces.king import King
from chess_pieces.knight import Knight
from chess_pieces.pawn import Pawn
from chess_pieces.queen import Queen
from chess_pieces.rook import Rook
from errors.exceptions import InvalidPieceError
from tools.constants import PieceColor


class ChessBoard:
    def __init__(self):
        self.__board = self.__create_board()  # sparse matrix representation
        self.__white_king = self[7, 4]
        self.__black_king = self[0, 4]

    def reinit(self):
        self.__init__()

    @property
    def occupied_cells(self):
        return list(self.__board)

    @property
    def whites(self):
        return self.getPieceOfColor(PieceColor.WHITE)

    @property
    def blacks(self):
        return self.getPieceOfColor(PieceColor.BLACK)

    def getPieceOfColor(self, color):
        returned_pieces = []
        for direction in self.__board:
            if self.__board[direction].color == color:
                returned_pieces.append(self.__board[direction])
        return returned_pieces

    def get_king(self, color):
        kings = {PieceColor.WHITE: self.__white_king, PieceColor.BLACK: self.__black_king}
        return kings[color] if color in kings else None

    def validate_move(self, x, y):
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        return True

    def __create_board(self):
        board = {}

        pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for row in range(2):
            for column in range(8):
                current_piece = Pawn(self, row, column, PieceColor.BLACK) if row == 1 else pieces[column](self, row, column, PieceColor.BLACK)
                board[(row, column)] = current_piece

        for row in range(6, 8):
            for column in range(8):
                current_piece = Pawn(self, row, column, PieceColor.WHITE) if row == 6 else pieces[column](self, row, column, PieceColor.WHITE)
                board[(row, column)] = current_piece
        return board

    def __getitem__(self, key):
        return None if key not in self.__board else self.__board[key]

    def __setitem__(self, key, piece):
        if piece is not None and type(piece) not in [Rook, Knight, Bishop, Queen, King, Pawn]:
            raise InvalidPieceError("'{}' is not a valid chess piece.".format(piece))
        if piece is None and key in self.__board:
            del self.__board[key]
        elif piece is not None:
            if (piece.x, piece.y) in self.__board:
                del self.__board[piece.x, piece.y]
            piece.x = key[0]
            piece.y = key[1]
            self.__board[key] = piece

    def __str__(self):
        """
            br/wr - black/white rook
            bh/wh - black/white knight (horse)
            bb/wb - black/white bishop
            bq/wq - black/white queen
            bk/wk - black/white king
            bp/wp - black/white pawn
        """
        black_pieces_dictionary = {Rook: 'br', Knight: 'bh', Bishop: 'bb', Queen: 'bq', King: 'bk', Pawn: 'bp'}
        white_pieces_dictionary = {Rook: 'wr', Knight: 'wh', Bishop: 'wb', Queen: 'wq', King: 'wk', Pawn: 'wp'}

        representation = Texttable()
        header = [''] + [str(index) for index in range(8)]
        representation.header(header)

        for row in range(8):
            row_data = [str(row)]
            for column in range(8):
                if self[row, column] is None:
                    row_data.append('')
                elif self[row, column].color == PieceColor.BLACK:
                    row_data.append(black_pieces_dictionary[type(self[row, column])])
                elif self[row, column].color == PieceColor.WHITE:
                    row_data.append(white_pieces_dictionary[type(self[row, column])])
            representation.add_row(row_data)
        return representation.draw()
