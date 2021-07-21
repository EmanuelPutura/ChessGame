import os

import pygame

from presentation.gui.constants import Colors, Dimensions
from tools.constants import PieceColor


class GameBoard(pygame.sprite.Sprite):
    def __init__(self, board, main_window, dimension=Dimensions.CHESSBOARD_CELLS.value, cell_colors=(Colors.WHITE, Colors.BLACK1)):
        super().__init__()

        self.__board = board
        self.__main_window = main_window
        self.__surface = pygame.Surface((dimension, dimension))
        self.__rectangle = self.__surface.get_rect()
        self.__dimension = dimension
        self.__cell_colors = cell_colors

        self.__chess_board_dimension = self.__main_window.get_size()[1] - Dimensions.MARGIN.value * 2
        self.__cell_dimension = self.__chess_board_dimension / self.__dimension

    @property
    def cell_dimension(self):
        return self.__cell_dimension

    def update(self):
        pass

    def __fill_cell(self, surface, row, column):
        if (row + column) % 2 == 0:
            surface.fill(self.__cell_colors[0].value)
        else:
            surface.fill(self.__cell_colors[1].value)

    def find_board_cell(self, window_x, window_y):
        margin = Dimensions.MARGIN.value

        if window_x < margin or window_y < margin or window_x > self.__chess_board_dimension + margin \
                or window_y > self.__chess_board_dimension + margin:
            return None
        return int((window_y - margin) // self.__cell_dimension), int((window_x - margin) // self.__cell_dimension)

    def draw(self):
        for row in range(self.__dimension):
            for column in range(self.__dimension):
                cell_surface = pygame.Surface((self.__cell_dimension, self.__cell_dimension))
                self.__fill_cell(cell_surface, row, column)
                cell_rectangle = cell_surface.get_rect(left=Dimensions.MARGIN.value + column * self.__cell_dimension,
                                                       top=Dimensions.MARGIN.value + row * self.__cell_dimension)
                self.__main_window.blit(cell_surface, cell_rectangle)
        self.__draw_pieces()

    def __draw_piece(self, file_name, position, cell_dimension):
        relative_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        image = pygame.image.load(relative_path + file_name)
        image = pygame.transform.scale(image, (int(cell_dimension), int(cell_dimension)))
        image.convert()

        self.__main_window.blit(image, position)

    def __draw_pieces(self):
        # black pieces dict
        black_pieces = {"pawn": r'\\assets\black_pawn.png', "rook": r'\\assets\black_rook.png', "knight": r'\\assets\black_knight.png',
                        "bishop": r'\\assets\black_bishop.png', "queen": r'\\assets\black_queen.png', "king": r'\\assets\black_king.png'}

        # white pieces dict
        white_pieces = {"pawn": r'\\assets\white_pawn.png', "rook": r'\\assets\white_rook.png', "knight": r'\\assets\white_knight.png',
                        "bishop": r'\\assets\white_bishop.png', "queen": r'\\assets\white_queen.png', "king": r'\\assets\white_king.png'}

        # match color to dictionary
        colors_dictionary = {PieceColor.WHITE: white_pieces, PieceColor.BLACK: black_pieces}

        for row in range(self.__dimension):
            for column in range(self.__dimension):
                if self.__board[row, column] is not None:
                    piece = self.__board[row, column]
                    piece_colour, piece_name = piece.name.split()[0], piece.name.split()[1]
                    self.__draw_piece(colors_dictionary[piece.color][piece_name], (Dimensions.MARGIN.value + column * self.__cell_dimension,
                                      Dimensions.MARGIN.value + row * self.__cell_dimension), self.__cell_dimension)
