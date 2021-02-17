from texttable import Texttable


class ChessBoard:
    def __init__(self):
        self.__board = self.__create_board()

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
        empty_cells = [[None] * 8] * 4
        black_pieces = [[15, 15, 15, 15, 15, 15, 15, 15],
                        [10, 11, 12, 13, 14, 12, 11, 10]]
        board = white_pieces + empty_cells + black_pieces
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
            .     - no piece
        """
        pieces_dictionary = {None: '', 0: 'br', 1: 'bh', 2: 'bb', 3: 'bq', 4: 'bk', 5: 'bp',
                                10: 'wr', 11: 'wh', 12: 'wb', 13: 'wq', 14: 'wk', 15: 'wp'}
        representation = Texttable()
        header = [''] + [chr(ord('A') + index) for index in range(8)]
        representation.header(header)

        for row in range(8):
            row_data = [str(row + 1)] + [pieces_dictionary[self.__board[row][column]] for column in range(8)]
            representation.add_row(row_data)
        return representation.draw()
