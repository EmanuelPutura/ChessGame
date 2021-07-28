from chess_board.board import ChessBoard
from chess_pieces.king import King
from errors.exceptions import InvalidMoveError
from tools.constants import PieceColor


class GameService:
    def __init__(self):
        self.__chess_board = ChessBoard()
        self.__white_king = self.__chess_board.get_king(PieceColor.WHITE)
        self.__black_king = self.__chess_board.get_king(PieceColor.BLACK)
        self.__white_pieces = self.__find_pieces(PieceColor.WHITE)
        self.__black_pieces = self.__find_pieces(PieceColor.BLACK)

    @property
    def board(self):
        return self.__chess_board

    def __find_pieces(self, color):
        pieces = []
        for cell in self.__chess_board.occupied_cells:
            if self.__chess_board[cell].color == color:
                pieces.append(self.__chess_board[cell])
        return pieces

    def __check(self, enemy_color):
        king_color_dictionary = {PieceColor.WHITE: self.__black_king, PieceColor.BLACK: self.__white_king}
        king = king_color_dictionary[enemy_color]
        return not king.check_safe(king.x, king.y)

    def getPiece(self, x, y):
        return self.__chess_board[x, y]

    def __checkmate(self, enemy_color, check_value):
        if not check_value:
            return False

        # get the king to be checked
        king_color_dictionary = {PieceColor.WHITE: self.__black_king, PieceColor.BLACK: self.__white_king}
        king = king_color_dictionary[enemy_color]

        # case 1: try to escape by moving to a free cell
        options = king.get_move_options()
        for option in options:
            if self.__chess_board[option] is None:
                return False

    def move(self, source_x, source_y, destination_x, destination_y, moving_color):
        if self.__chess_board[source_x, source_y] is None:
            raise InvalidMoveError('InvalidMoveError: No piece at coordinates ({}, {}).'.format(source_x, source_y))
        piece = self.__chess_board[source_x, source_y]
        if piece.color != moving_color:
            raise InvalidMoveError('InvalidMoveError: The selected piece is not yours.')

        piece.move(destination_x, destination_y)

        # get the enemy king, which might be in check after the move
        king_color_dictionary = {PieceColor.WHITE: self.__black_king, PieceColor.BLACK: self.__white_king}
        king = king_color_dictionary[moving_color]

        check = self.__check(moving_color)
        # checkmate = self.__check(moving_color) and king.get_move_options() == []
        # print("Check: {}, Checkmate: {}".format(check, checkmate))
