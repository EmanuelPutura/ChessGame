from chess_board.board import ChessBoard
from chess_pieces.king import King
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class GameService:
    def __init__(self):
        self.__chess_board = ChessBoard()
        self.__white_king = self.__search_king(PieceColor.WHITE)
        self.__black_king = self.__search_king(PieceColor.BLACK)
        self.__white_pieces = self.__find_pieces(PieceColor.WHITE)
        self.__black_pieces = self.__find_pieces(PieceColor.BLACK)

    @property
    def board(self):
        return self.__chess_board

    def __find_pieces(self, color):
        pieces = []
        for row in range(8):
            for column in range(8):
                if self.__chess_board[row][column] is not None and self.__chess_board[row][column].color == color:
                    pieces.append(self.__chess_board[row][column])
        return pieces

    def __search_king(self, color):
        for row in range(8):
            for column in range(8):
                if type(self.__chess_board[row][column]) is King and self.__chess_board[row][column].color == color:
                    return self.__chess_board[row][column]
        return None

    def __check(self, color):
        king_color_dictionary = {PieceColor.WHITE: self.__white_king, PieceColor.BLACK: self.__black_king}
        king = king_color_dictionary[color]
        piece_color_dictionary = {PieceColor.WHITE: self.__black_pieces, PieceColor.BLACK: self.__white_pieces}
        for piece in piece_color_dictionary[color]:
            if piece.attempt_move(king.x, king.y):
                return True
        return False

    def __checkmate(self, moving_color):
        king_color_dictionary = {PieceColor.WHITE: self.__white_king, PieceColor.BLACK: self.__black_king}
        piece_opposite_color_dictionary = {PieceColor.WHITE: self.__black_pieces, PieceColor.BLACK: self.__white_pieces}
        piece_color_dictionary = {PieceColor.WHITE: self.__white_pieces, PieceColor.BLACK: self.__black_pieces}
        king = king_color_dictionary[moving_color]
        directions = [-1, 0, 1]

        king_x, king_y = king.x, king.y
        for direction_x in directions:
            for direction_y in directions:
                if direction_x == direction_y == 0:
                    continue
                current_x = king_x + direction_x
                current_y = king_y + direction_y
                try:
                    king.move(current_x, current_y)
                    self.__chess_board[king_x][king_y] = None
                    last_piece = self.__chess_board[current_x][current_y]
                    self.__chess_board[current_x][current_y] = king

                    if last_piece is not None:
                        piece_opposite_color_dictionary[moving_color].remove(last_piece)
                    check = self.__check(moving_color)

                    king.move(king_x, king_y)
                    self.__chess_board[king_x][king_y] = king
                    self.__chess_board[current_x][current_y] = last_piece

                    if last_piece is not None:
                        piece_opposite_color_dictionary[moving_color].append(last_piece)

                    if not check:
                        return False
                except InvalidMoveError:
                    pass
                # for piece in piece_color_dictionary[moving_color]:
                # TODO: case when check is blocked by moving a new piece
        return True

    def getPiece(self, x, y):
        return self.__chess_board[x][y]

    def move(self, source_x, source_y, destination_x, destination_y, moving_color):
        # get the current color king
        king_color_dictionary = {PieceColor.WHITE: self.__white_king, PieceColor.BLACK: self.__black_king}
        king = king_color_dictionary[moving_color]

        check = self.__check(moving_color)

        if self.__chess_board[source_x][source_y] is None:
            raise InvalidMoveError('InvalidMoveError: No piece at coordinates ({}, {}).'.format(source_x, source_y))
        piece = self.__chess_board[source_x][source_y]
        if piece.color != moving_color:
            raise InvalidMoveError('InvalidMoveError: The selected piece is not yours.')

        piece.move(destination_x, destination_y)
        self.__chess_board[source_x][source_y] = None
        last_piece = self.__chess_board[destination_x][destination_y]
        self.__chess_board[destination_x][destination_y] = piece

        if last_piece is not None:
            piece_color_dictionary = {PieceColor.WHITE: self.__black_pieces, PieceColor.BLACK: self.__white_pieces}
            piece_color_dictionary[moving_color].remove(last_piece)

        if self.__check(moving_color):
            piece.move(source_x, source_y)
            self.__chess_board[source_x][source_y] = piece
            self.__chess_board[destination_x][destination_y] = last_piece

            if last_piece is not None:
                piece_color_dictionary = {PieceColor.WHITE: self.__black_pieces, PieceColor.BLACK: self.__white_pieces}
                piece_color_dictionary[moving_color].append(last_piece)

            if check:
                raise InvalidMoveError('Check! You must move your king!')
            raise InvalidMoveError('Impossible move: check!')

        opposite_color_dictionary = {PieceColor.WHITE: PieceColor.BLACK, PieceColor.BLACK: PieceColor.WHITE}
        if self.__check(opposite_color_dictionary[moving_color]) and self.__checkmate(opposite_color_dictionary[moving_color]):
            return True
        return False
