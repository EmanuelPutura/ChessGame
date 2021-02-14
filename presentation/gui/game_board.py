import os

import pygame

from presentation.gui.constants import Colors, Dimensions


class GameBoard(pygame.sprite.Sprite):
    def __init__(self, main_window, dimension=8, cell_colors=(Colors.WHITE, Colors.BLACK1)):
        super().__init__()

        self.__main_window = main_window
        self.__surface = pygame.Surface((dimension, dimension))
        self.__rectangle = self.__surface.get_rect()
        self.__dimension = dimension
        self.__cell_colors = cell_colors

        self.__chess_board_dimension = self.__main_window.get_size()[1] - Dimensions.MARGIN.value * 2
        self.__cell_dimension = self.__chess_board_dimension / self.__dimension

    def update(self):
        pass

    def __fill_cell(self, surface, row, column):
        if (row + column) % 2 == 0:
            surface.fill(self.__cell_colors[0].value)
        else:
            surface.fill(self.__cell_colors[1].value)

    def find_board_cell(self, window_x, window_y):
        margin = Dimensions.MARGIN.value

        if window_x < margin or window_y < margin or window_x > self.__chess_board_dimension - margin \
                or window_y > window_x > self.__chess_board_dimension - margin:
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
        # draw the black pawns
        for column in range(self.__dimension):
            self.__draw_piece(r'\\assets\black_pawn.png', (Dimensions.MARGIN.value + column * self.__cell_dimension,
                                                           Dimensions.MARGIN.value + self.__cell_dimension), self.__cell_dimension)

        # draw the white pawns
        for column in range(self.__dimension):
            self.__draw_piece(r'\\assets\white_pawn.png', (Dimensions.MARGIN.value + column * self.__cell_dimension,
                                                           Dimensions.MARGIN.value + self.__cell_dimension * (
                                                                       self.__dimension - 2)), self.__cell_dimension)

        # draw the black rooks
        self.__draw_piece(r'\\assets\black_rook.png', (Dimensions.MARGIN.value, Dimensions.MARGIN.value),
                          self.__cell_dimension)
        self.__draw_piece(r'\\assets\black_rook.png', (Dimensions.MARGIN.value +
                                                       self.__cell_dimension * (self.__dimension - 1),
                                                       Dimensions.MARGIN.value), self.__cell_dimension)

        # draw the white rooks
        self.__draw_piece(r'\\assets\white_rook.png', (Dimensions.MARGIN.value, Dimensions.MARGIN.value +
                                                       self.__cell_dimension * (self.__dimension - 1)), self.__cell_dimension)

        self.__draw_piece(r'\\assets\white_rook.png',
                          (Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 1),
                           Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 1)), self.__cell_dimension)

        # draw the black knights
        self.__draw_piece(r'\\assets\black_knight.png', (Dimensions.MARGIN.value + self.__cell_dimension,
                                                         Dimensions.MARGIN.value), self.__cell_dimension)
        self.__draw_piece(r'\\assets\black_knight.png',
                          (Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 2),
                           Dimensions.MARGIN.value), self.__cell_dimension)

        # draw the white knights
        self.__draw_piece(r'\\assets\white_knight.png', (Dimensions.MARGIN.value + self.__cell_dimension,
                                                         Dimensions.MARGIN.value + self.__cell_dimension * (
                                                                     self.__dimension - 1)), self.__cell_dimension)
        self.__draw_piece(r'\\assets\white_knight.png',
                          (Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 2),
                           Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 1)), self.__cell_dimension)

        # draw the black bishops
        self.__draw_piece(r'\\assets\black_bishop.png', (Dimensions.MARGIN.value + self.__cell_dimension * 2,
                                                         Dimensions.MARGIN.value), self.__cell_dimension)
        self.__draw_piece(r'\\assets\black_bishop.png',
                          (Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 3),
                           Dimensions.MARGIN.value), self.__cell_dimension)

        # draw the white bishops
        self.__draw_piece(r'\\assets\white_bishop.png', (Dimensions.MARGIN.value + self.__cell_dimension * 2,
                                                         Dimensions.MARGIN.value + self.__cell_dimension * (
                                                                     self.__dimension - 1)), self.__cell_dimension)
        self.__draw_piece(r'\\assets\white_bishop.png',
                          (Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 3),
                           Dimensions.MARGIN.value + self.__cell_dimension * (self.__dimension - 1)), self.__cell_dimension)

        # draw the black queen
        self.__draw_piece(r'\\assets\black_queen.png', (Dimensions.MARGIN.value + self.__cell_dimension * 3,
                                                        Dimensions.MARGIN.value), self.__cell_dimension)

        # draw the white queen
        self.__draw_piece(r'\\assets\white_queen.png', (Dimensions.MARGIN.value + self.__cell_dimension * 3,
                                                        Dimensions.MARGIN.value + self.__cell_dimension * (
                                                                    self.__dimension - 1)), self.__cell_dimension)

        # draw the black king
        self.__draw_piece(r'\\assets\black_king.png', (Dimensions.MARGIN.value + self.__cell_dimension * 4,
                                                       Dimensions.MARGIN.value), self.__cell_dimension)

        # draw the white king
        self.__draw_piece(r'\\assets\white_king.png', (Dimensions.MARGIN.value + self.__cell_dimension * 4,
                                                       Dimensions.MARGIN.value + self.__cell_dimension * (
                                                                   self.__dimension - 1)), self.__cell_dimension)
