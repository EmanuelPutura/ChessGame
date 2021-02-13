import pygame

from presentation.gui.constants import Colors, Dimensions
from presentation.gui.game_board import GameBoard


class MainWindow:
    def __init__(self):
        pygame.init()
        self.__window = pygame.display.set_mode((Dimensions.WINDOW_LENGTH.value, Dimensions.WINDOW_HEIGHT.value))
        self.__window.fill(Colors.BLACK2.value)
        self.__draw_margin()
        self.__game_board = GameBoard(self.__window)

    def __draw_margin(self):
        line_dictionary = {0: ((37, 37), (662, 37)), 1: ((660, 37), (660, 660)), 2: ((660, 660), (37, 660)),
                           3: ((37, 37), (37, 660))}
        lines_number = 4
        for index in range(lines_number):
            start = line_dictionary[index][0]
            end = line_dictionary[index][1]
            pygame.draw.line(self.__window, Colors.BLACK1.value, start, end, 4)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
            self.__game_board.update()
            pygame.display.flip()
        pygame.quit()


gui = MainWindow()
gui.run()
