from chess_board.board import ChessBoard
from chess_pieces.bishop import Bishop
from chess_pieces.knight import Knight
from chess_pieces.queen import Queen
from chess_pieces.rook import Rook
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

    def checkmate(self, color):
        piece_mapping = {PieceColor.WHITE: self.__chess_board.whites, PieceColor.BLACK: self.__chess_board.blacks}
        for piece in piece_mapping[color]:
            if piece.get_move_options():
                return False
        return True

    def move(self, source_x, source_y, destination_x, destination_y, moving_color):
        if self.__chess_board[source_x, source_y] is None:
            raise InvalidMoveError('InvalidMoveError: No piece at coordinates ({}, {}).'.format(source_x, source_y))
        piece = self.__chess_board[source_x, source_y]
        if piece.color != moving_color:
            raise InvalidMoveError('InvalidMoveError: The selected piece is not yours.')

        piece.move(destination_x, destination_y)
        enemy_color = PieceColor.WHITE if moving_color == PieceColor.BLACK else PieceColor.BLACK
        if self.checkmate(enemy_color):
            return True
        return False

    def check_pawn_reached_table_end(self, piece):
        if piece.__class__.__name__ == 'Pawn':
            if piece.color == PieceColor.WHITE and piece.x == 0:
                return True
            elif piece.color == PieceColor.BLACK and piece.x == 7:
                return True
            else:
                return False
        return False

    def pawn_reached_table_end(self, pawn, new_piece):
        if new_piece is None:
            return
        piece_dictionary = {'Bishop': Bishop, 'Knight': Knight, 'Rook': Rook, 'Queen': Queen}
        new_piece = piece_dictionary[new_piece](self.__chess_board, pawn.x, pawn.y, pawn.color)
        self.__chess_board[pawn.x, pawn.y] = new_piece
