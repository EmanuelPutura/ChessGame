from texttable import Texttable

from chess_pieces.bishop import Bishop
from chess_pieces.king import King
from chess_pieces.knight import Knight
from chess_pieces.pawn import Pawn
from chess_pieces.queen import Queen
from chess_pieces.rook import Rook
from tools.constants import PieceColor


class ChessBoard:
    def __init__(self):
        self.__board = self.__create_board()

    def validate_move(self, x, y):
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        return True

    def __create_board(self):
        """
            black/white rook   - code 0/10
            black/white knight - code 1/11
            black/white bishop - code 2/12
            black/white queen  - code 3/13
            black/white king   - code 4/14
            black/white pawn   - code 5/15
            no piece           - None
        """

        white_pieces = [[0, 1, 2, 3, 4, 2, 1, 0],
                        [5, 5, 5, 5, 5, 5, 5, 5]]
        empty_cells = [[None for column in range(8)] for row in range(4)]
        black_pieces = [[15, 15, 15, 15, 15, 15, 15, 15],
                        [10, 11, 12, 13, 14, 12, 11, 10]]
        board = white_pieces + empty_cells + black_pieces

        pieces_dictionary = {0: Rook, 1: Knight, 2: Bishop, 3: Queen, 4: King, 5: Pawn,
                             10: Rook, 11: Knight, 12: Bishop, 13: Queen, 14: King, 15: Pawn}
        # black pieces
        for row in range(2):
            for column in range(8):
                board[row][column] = pieces_dictionary[board[row][column]](self, row, column, PieceColor.BLACK)
        # white pieces
        for row in range(6, 8):
            for column in range(8):
                board[row][column] = pieces_dictionary[board[row][column]](self, row, column, PieceColor.WHITE)
        return board

    def __getitem__(self, key):
        return self.__board[key]

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
                if self.__board[row][column] is None:
                    row_data.append('')
                elif self.__board[row][column].color == PieceColor.BLACK:
                    row_data.append(black_pieces_dictionary[type(self.__board[row][column])])
                elif self.__board[row][column].color == PieceColor.WHITE:
                    row_data.append(white_pieces_dictionary[type(self.__board[row][column])])
            representation.add_row(row_data)
        return representation.draw()
