import os
import tkinter
from tkinter import messagebox

import pygame

from errors.exceptions import UserInputError, InvalidVerificationCodeError
from presentation.gui.constants import Colors, Dimensions
from presentation.gui.game_board import GameBoard
from presentation.gui.gradient_generator import GradientGenerator
from presentation.gui.piece_choice_window import PieceChoiceWindow
from presentation.gui.widgets import Label, ImageButton, TextBox, CreateAccountTextButton, BackImageButton, \
    LoginImageButton, ExitImageButton, PlayAsGuestImageButton, DefaultImageButton, RestartImageButton
from tools.constants import PieceColor
from tools.validators import CredentialsValidator
from tools.email_sender import EmailSender


class MainWindow:
    def __init__(self, game_service, users_service):
        pygame.init()
        self.__game_service = game_service
        self.__users_service = users_service

        self.__white_turn = True
        self.__current_piece = None

        self.__window = pygame.display.set_mode((Dimensions.WINDOW_WIDTH.value, Dimensions.WINDOW_HEIGHT.value))
        pygame.display.set_caption('Quess')
        self.__window.fill(Colors.BLACK2.value)
        self.__gradient_generator = GradientGenerator(self.__window, Colors.BLACK3.value, Colors.BLACK2.value)
        self.__gradient_generator.fill_gradient(True)
        self.__draw_margin()
        self.__game_board = GameBoard(self.__game_service.board, self.__window)
        self.__widgets_group = pygame.sprite.Group()

        self.__turn_label = None
        self.__winner_button = None
        self.__sign_up_button = None
        self.__signup_email_textbox = None
        self.__signup_username_textbox = None
        self.__signup_password_textbox = None
        self.__signup_repeated_password_textbox = None
        self.__verification_textbox = None
        self.__submit_button = None
        self.__code = None
        self.__login_username_textbox = None
        self.__login_password_textbox = None

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

        self.__sign_up_button = None
        self.__signup_email_textbox = None
        self.__signup_username_textbox = None
        self.__signup_password_textbox = None
        self.__signup_repeated_password_textbox = None
        self.__verification_textbox = None
        self.__submit_button = None
        self.__code = None

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
        self.__login_username_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        self.__login_username_textbox.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        self.__login_password_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        self.__login_password_textbox.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        create_account_button = CreateAccountTextButton(self, 'Create an account', widget_font, widget_width, widget_height, widget_x, widget_y)
        create_account_button.add(self.__widgets_group)

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_y = widget_y + widget_height + cell_dimension + margin
        guest_button = PlayAsGuestImageButton(self, r'\\assets\guest.png', widget_width, widget_height, widget_x, widget_y)
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
        self.__sign_up_button = ImageButton(self, r'\\assets\sign_up.png', widget_width, widget_height, widget_x, widget_y)
        self.__sign_up_button.add(self.__widgets_group)

        widget_x -= 20
        widget_y = widget_y + widget_height + 10
        logged_in_label = Label(self, 'Email address:', widget_font, widget_width, widget_height, widget_x, widget_y)
        logged_in_label.add(self.__widgets_group)

        widget_width += 40
        self.__signup_email_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        self.__signup_email_textbox.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Username:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        self.__signup_username_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        self.__signup_username_textbox.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        self.__signup_password_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        self.__signup_password_textbox.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        password_label = Label(self, 'Repeat password:', widget_font, widget_width, widget_height, widget_x, widget_y)
        password_label.add(self.__widgets_group)

        self.__signup_repeated_password_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, True, '', widget_font)
        self.__signup_repeated_password_textbox.add(self.__widgets_group)

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

    def init_play_as_guest_widgets(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension
        widget_font = pygame.font.SysFont('Benne', 20)

        widget_x = screen_height + 22.5
        widget_width = 110
        widget_height = 110

        get_widget_y = lambda middle, height: middle - height / 2
        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height) + margin

        widget_x -= 5
        widget_y = widget_y + widget_height + 10

        if self.__winner_button is None:
            self.__init_turn_label()
        else:
            self.__init_winner_button()

        widget_x = screen_height
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_y = widget_y + widget_height + cell_dimension + margin

        widget_y = widget_y + widget_height + 150

        widget_y = widget_y - widget_height - 10
        restart_button = RestartImageButton(self, r'\\assets\restart.png', widget_width, widget_height, widget_x, widget_y)
        restart_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        back_button = BackImageButton(self, r'\\assets\back.png', widget_width, widget_height, widget_x, widget_y)
        back_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        exit_button = ExitImageButton(self, r'\\assets\exit.png', widget_width, widget_height, widget_x, widget_y)
        exit_button.add(self.__widgets_group)

    def __init_turn_label(self):
        widget_font = pygame.font.SysFont('Benne', 20)
        widget_width = 110
        widget_height = 110
        turn_map = {False: 'Current turn: black player', True: 'Current turn: white player'}

        self.__turn_label = Label(self, turn_map[self.__white_turn], widget_font, widget_width, widget_height,
                                  Dimensions.MARGIN.value, Dimensions.MARGIN.value - 20, Colors.WHITE.value)
        self.__turn_label.add(self.__widgets_group)

    def __init_winner_button(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension

        widget_x = screen_height + 2.5
        widget_width = 150
        widget_height = 110

        get_widget_y = lambda middle, height: middle - height / 2
        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height) + margin

        winner_mapping = {True: r'\\assets\black_win.png', False: r'\\assets\white_win.png'}

        self.__winner_button = DefaultImageButton(self, winner_mapping[self.__white_turn], widget_width, widget_height, widget_x, widget_y)
        self.__winner_button.add(self.__widgets_group)

    def __draw_piece_move_options(self, piece):
        for move in piece.get_move_options():
            self.__draw_circle_in_cell_middle(move[0], move[1])

    def __draw_circle_in_cell_middle(self, row, column):
        cell_dimension = (self.__window.get_size()[1] - Dimensions.MARGIN.value * 2) / Dimensions.CHESSBOARD_CELLS.value
        x = Dimensions.MARGIN.value + column * cell_dimension
        y = Dimensions.MARGIN.value + row * cell_dimension
        center = (x + cell_dimension / 2, y + cell_dimension / 2)
        pygame.draw.circle(self.__window, Colors.GRAY.value, center, 10)

    def __draw_margin(self):
        line_dictionary = {0: ((37, 37), (662, 37)), 1: ((660, 37), (660, 660)), 2: ((660, 660), (37, 660)),
                           3: ((37, 37), (37, 660))}
        lines_number = 4
        for index in range(lines_number):
            start = line_dictionary[index][0]
            end = line_dictionary[index][1]
            pygame.draw.line(self.__window, Colors.BLACK1.value, start, end, 4)

    def restart_game(self):
        self.__white_turn = True
        self.__current_piece = None
        self.__game_service.board.reinit()
        self.__game_board = GameBoard(self.__game_service.board, self.__window)
        if self.__winner_button is not None:
            self.__widgets_group.remove(self.__winner_button)
            self.__winner_button = None
            self.__init_turn_label()
        if self.__turn_label is not None:
            turn_map = {False: 'Current turn: black player', True: 'Current turn: white player'}
            self.__turn_label.text = turn_map[self.__white_turn]

    def __sign_up_button_clicked(self):
        email = self.__signup_email_textbox.text
        username = self.__signup_username_textbox.text
        password = self.__signup_password_textbox.text
        repeated_password = self.__signup_repeated_password_textbox.text
        CredentialsValidator.validate(email, username, password, repeated_password, self.__users_service)

        sender = EmailSender()
        sender.send(username, email)
        self.__code = sender.code

        self.__widgets_group.empty()
        self.__sign_up_button = None

        screen_width, screen_height = pygame.display.get_surface().get_size()
        margin = Dimensions.MARGIN.value
        cell_dimension = self.__game_board.cell_dimension

        widget_x = screen_height - 20
        widget_width = screen_width - screen_height - margin
        widget_height = margin
        widget_font = pygame.font.SysFont('Benne', 20)

        get_widget_y = lambda middle, height: middle - height / 2
        widget_y = get_widget_y(margin + cell_dimension / 2, widget_height)

        verification_label = Label(self, 'Email verification code:', widget_font, widget_width, widget_height, widget_x, widget_y)
        verification_label.add(self.__widgets_group)

        widget_width += 40
        self.__verification_textbox = TextBox(widget_x, widget_y, widget_width, widget_height, False, '', widget_font)
        self.__verification_textbox.add(self.__widgets_group)

        widget_width -= 40
        widget_x += 20
        widget_y = widget_y + widget_height + 10
        self.__submit_button = ImageButton(self, r'\\assets\submit.png', widget_width, widget_height, widget_x, widget_y)
        self.__submit_button.add(self.__widgets_group)

        widget_y = widget_y + widget_height + 10
        back_button = BackImageButton(self, r'\\assets\main_menu.png', widget_width, widget_height, widget_x, widget_y)
        back_button.add(self.__widgets_group)

    def __submit_button_clicked(self):
        email = self.__signup_email_textbox.text
        username = self.__signup_username_textbox.text
        password = self.__signup_password_textbox.text
        code = self.__verification_textbox.text

        if str(self.__code) != code:
            raise InvalidVerificationCodeError("Invalid verification code!")

        self.__users_service.insert(email, username, password)
        self.__widgets_group.empty()
        self.init_widgets()

    def attempt_login(self):
        username = self.__login_username_textbox.text
        password = self.__login_password_textbox.text
        self.__users_service.attempt_login(username, password)
        self.__widgets_group.empty()
        self.init_login_widgets()

    def run(self):
        draw_options = False
        running = True
        while running:
            try:
                for event in pygame.event.get():

                    for widget in self.__widgets_group:
                        running = widget.update(event)
                        if not running:
                            break

                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.__sign_up_button is not None and self.__sign_up_button.rectangle.collidepoint(event.pos):
                            self.__sign_up_button_clicked()
                        if self.__submit_button is not None and self.__submit_button.rectangle.collidepoint(event.pos):
                            self.__submit_button_clicked()

                    if event.type == pygame.MOUSEBUTTONUP:
                        position = pygame.mouse.get_pos()
                        table_position = self.__game_board.find_board_cell(position[0], position[1])

                        if table_position is not None and self.__turn_label is not None:
                            moving_color = PieceColor.WHITE if self.__white_turn else PieceColor.BLACK

                            if self.__current_piece is not None and self.__current_piece.color == moving_color and table_position in self.__current_piece.get_move_options():
                                # make the move
                                self.__white_turn = not self.__white_turn
                                if self.__game_service.move(self.__current_piece.x, self.__current_piece.y, table_position[0], table_position[1], moving_color):
                                    self.__widgets_group.remove(self.__turn_label)
                                    self.__turn_label = None
                                    self.__init_winner_button()

                                # if the pawn reached the end of the table, let the player choose a new piece
                                if self.__game_service.check_pawn_reached_table_end(self.__current_piece):
                                    choice_window = PieceChoiceWindow(self.__current_piece.color)
                                    self.__game_service.pawn_reached_table_end(self.__current_piece, choice_window.piece)

                                if self.__turn_label is not None:
                                    turn_map = {PieceColor.WHITE: 'Current turn: black player', PieceColor.BLACK: 'Current turn: white player'}
                                    self.__turn_label.text = turn_map[moving_color]

                                self.__current_piece = None
                            else:
                                self.__current_piece = self.__game_service.getPiece(table_position[0], table_position[1])
                            if self.__current_piece is not None and self.__current_piece.color == moving_color and self.__turn_label is not None:
                                draw_options = True
                                self.__draw_piece_move_options(self.__current_piece)
                            else:
                                draw_options = False

                self.__window.fill(Colors.BLACK2.value)
                self.__gradient_generator.fill_gradient(True)
                self.__draw_margin()

                self.__game_board.draw()

                if self.__current_piece is not None and draw_options:
                    self.__draw_piece_move_options(self.__current_piece)

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
