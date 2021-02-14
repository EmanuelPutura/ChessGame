import pygame

from presentation.gui.constants import Colors, Dimensions
from presentation.gui.game_board import GameBoard
from presentation.gui.gradient_generator import GradientGenerator
from presentation.gui.widgets import Label, ImageButton, TextBox, TextButton


class MainWindow:
    def __init__(self):
        pygame.init()
        self.__window = pygame.display.set_mode((Dimensions.WINDOW_WIDTH.value, Dimensions.WINDOW_HEIGHT.value))
        pygame.display.set_caption('Quess')
        self.__window.fill(Colors.BLACK2.value)
        self.__gradient_generator = GradientGenerator(self.__window, Colors.BLACK3.value, Colors.BLACK2.value)
        self.__gradient_generator.fill_gradient(True)
        self.__draw_margin()
        self.__game_board = GameBoard(self.__window)
        self.__widgets_group = pygame.sprite.Group()
        self.__init_widgets()
        # self.__txtBox = TextBox(0, 0, 100, 50, 'Hello There!')
        # self.__txtBox.draw(self.__window)

    def __init_widgets(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_font = pygame.font.SysFont('Benne', 20)

        get_widget_y = lambda middle, height: middle - height / 2

        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height)
        self.__login_button = ImageButton(r'\\assets\login.png', widget_width, widget_height, widget_x, widget_y)
        self.__login_button.add(self.__widgets_group)

        widget_x -= 20
        widget_y = widget_y + widget_height + 10
        self.__username_label = Label('Username:', widget_font, widget_width, widget_height, widget_x, widget_y)
        self.__username_label.add(self.__widgets_group)

        widget_width += 40
        self.__username_text = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        self.__username_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        self.__password_label = Label('Password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        self.__password_label.add(self.__widgets_group)

        self.__password_text = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        self.__password_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        self.__create_account_button = TextButton('Create an account', widget_font, widget_width, widget_height, widget_x, widget_y)
        self.__create_account_button.add(self.__widgets_group)

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_y = widget_y + widget_height + cell_dimension + margin
        self.__guest_button = ImageButton(r'\\assets\guest.png', widget_width, widget_height, widget_x, widget_y)
        self.__guest_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        self.__tutorial_button = ImageButton(r'\\assets\tutorial.png', widget_width, widget_height, widget_x, widget_y)
        self.__tutorial_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        self.__settings_button = ImageButton(r'\\assets\settings.png', widget_width, widget_height, widget_x, widget_y)
        self.__settings_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        self.__exit_button = ImageButton(r'\\assets\exit.png', widget_width, widget_height, widget_x, widget_y)
        self.__exit_button.add(self.__widgets_group)

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

                for widget in self.__widgets_group:
                    widget.update(event)

                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()

            self.__window.fill(Colors.BLACK2.value)
            self.__gradient_generator.fill_gradient(True)
            self.__draw_margin()

            self.__game_board.draw()

            for widget in self.__widgets_group:
                widget.draw(self.__window)

            pygame.display.flip()
        pygame.quit()


gui = MainWindow()
gui.run()
