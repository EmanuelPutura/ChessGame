from chess_board.board import ChessBoard
from errors.exceptions import InvalidMoveError


class GameService:
    def __init__(self):
        self.__chess_board = ChessBoard()

    @property
    def board(self):
        return self.__chess_board

    def move(self, source_x, source_y, destination_x, destination_y, moving_color):
        if self.__chess_board[source_x][source_y] is None:
            raise InvalidMoveError('InvalidMoveError: No piece at coordinates ({}, {}).'.format(source_x, source_y))
        piece = self.__chess_board[source_x][source_y]
        if piece.color != moving_color:
            raise InvalidMoveError('InvalidMoveError: The selected piece is not yours.')
        piece.move(destination_x, destination_y)
        self.__chess_board[source_x][source_y] = None
        self.__chess_board[destination_x][destination_y] = piece
