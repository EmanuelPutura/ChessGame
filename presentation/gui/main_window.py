import os
import tkinter
from tkinter import messagebox

import pygame

from errors.exceptions import UserInputError
from presentation.gui.constants import Colors, Dimensions
from presentation.gui.game_board import GameBoard
from presentation.gui.gradient_generator import GradientGenerator
from presentation.gui.widgets import Label, ImageButton, TextBox, CreateAccountTextButton, BackImageButton, \
    LoginImageButton, ExitImageButton


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
        self.init_widgets()

    @property
    def widgets_group(self):
        return self.__widgets_group

    @property
    def window(self):
        return self.__window

    @property
    def game_board(self):
        return self.__game_board

    def init_widgets(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_font = pygame.font.SysFont('Benne', 20)

        get_widget_y = lambda middle, height: middle - height / 2

        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height)
        login_button = LoginImageButton(self, r'\\assets\login.png', widget_width, widget_height, widget_x, widget_y)
        login_button.add(self.__widgets_group)

        widget_x -= 20
        widget_y = widget_y + widget_height + 10
        logged_in_label = Label(self, 'Username:', widget_font, widget_width, widget_height, widget_x, widget_y)
        logged_in_label.add(self.__widgets_group)

        widget_width += 40
        username_text = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        username_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        password_text = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        password_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        create_account_button = CreateAccountTextButton(self, 'Create an account', widget_font, widget_width, widget_height, widget_x, widget_y)
        create_account_button.add(self.__widgets_group)

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_y = widget_y + widget_height + cell_dimension + margin
        guest_button = ImageButton(self, r'\\assets\guest.png', widget_width, widget_height, widget_x, widget_y)
        guest_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        tutorial_button = ImageButton(self, r'\\assets\tutorial.png', widget_width, widget_height, widget_x, widget_y)
        tutorial_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        settings_button = ImageButton(self, r'\\assets\settings.png', widget_width, widget_height, widget_x, widget_y)
        settings_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        exit_button = ExitImageButton(self, r'\\assets\exit.png', widget_width, widget_height, widget_x, widget_y)
        exit_button.add(self.__widgets_group)

    def init_account_widgets(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_font = pygame.font.SysFont('Benne', 20)

        get_widget_y = lambda middle, height: middle - height / 2

        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height)
        sign_up_button = ImageButton(self, r'\\assets\sign_up.png', widget_width, widget_height, widget_x, widget_y)
        sign_up_button.add(self.__widgets_group)

        widget_x -= 20
        widget_y = widget_y + widget_height + 10
        logged_in_label = Label(self, 'Email address:', widget_font, widget_width, widget_height, widget_x, widget_y)
        logged_in_label.add(self.__widgets_group)

        widget_width += 40
        username_text = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        username_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Username:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        password_text = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        password_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        password_text = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        password_text.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Repeat password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        password_text = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        password_text.add(self.__widgets_group)

        widget_x += 20
        widget_y = widget_y + widget_height + 10
        widget_width -= 40
        back_button = BackImageButton(self, r'\\assets\back.png', widget_width, widget_height, widget_x, widget_y)
        back_button.add(self.__widgets_group)

    def init_login_widgets(self):
        relative_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        avatar_image = pygame.image.load(relative_path + r'\\assets\avatar.png')

        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension
        widget_font = pygame.font.SysFont('Benne', 20)

        widget_x = screen_height + 22.5
        widget_width = 110
        widget_height = 110

        get_widget_y = lambda middle, height: middle - height / 2
        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height) + margin

        avatar_image = ImageButton(self, r'\\assets\avatar.png', widget_width, widget_height, widget_x, widget_y)
        avatar_image.add(self.__widgets_group)

        widget_x -= 5
        widget_y = widget_y + widget_height + 10

        logged_in_label = Label(self, 'Currently logged in', widget_font, widget_width, widget_height, widget_x,
                                     widget_y, Colors.GRAY.value)
        logged_in_label.add(self.__widgets_group)

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_y = widget_y + widget_height + cell_dimension + margin
        play_button = ImageButton(self, r'\\assets\play.png', widget_width, widget_height, widget_x, widget_y)
        play_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        tutorial_button = ImageButton(self, r'\\assets\tutorial.png', widget_width, widget_height, widget_x, widget_y)
        tutorial_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        settings_button = ImageButton(self, r'\\assets\settings.png', widget_width, widget_height, widget_x, widget_y)
        settings_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        back_button = BackImageButton(self, r'\\assets\back.png', widget_width, widget_height, widget_x, widget_y)
        back_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        exit_button = ExitImageButton(self, r'\\assets\exit.png', widget_width, widget_height, widget_x, widget_y)
        exit_button.add(self.__widgets_group)

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
            try:
                for event in pygame.event.get():

                    for widget in self.__widgets_group:
                        running = widget.update(event)

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
            except UserInputError as userInputError:
                tkinter.Tk().wm_withdraw()
                messagebox.showwarning('UserInputError', userInputError)
            # except Exception as exception:
            #     tkinter.Tk().wm_withdraw()
            #     messagebox.showwarning('Unexpected exception', exception)
        pygame.quit()
