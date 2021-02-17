from errors.exceptions import UserInputError, InvalidMoveError
from tools.constants import PieceColor


class ConsoleUI:
    def __init__(self, game_service):
        self.__game_service = game_service
        self.__commands = {'move': self.__move_command, 'help': self.__help_command}
        self.__white_turn = True

    def __print_menu(self):
        print('-' * 20 + 'Quess - a chess game' + '-' * 20)
        print(' move - make a move')
        print(' help - get help regarding how to play the game')
        print('-' * 60 + '\n')

    def __print_board(self):
        print('The current game board is:')
        print(self.__game_service.board)
        turn_dictionary = {True: 'White', False: 'Black'}
        print("{}'s turn:\n".format(turn_dictionary[self.__white_turn]))

    def __help_command(self):
        print('move - attempt to make a move on the chess game.\n      You will be asked to input the board coordinates of the piece'
              'you want to move and the coordinates of the position where you want to move the piece.\n      Board coordinates start from the'
              'up and left part of the board, with zero.')
        print('br/wr - black/white rook\nbh/wh - black/white knight (horse)\n'
              'bb/wb - black/white bishop\nbq/wq - black/white queen\nbk/wk - black/white king\nbp/wp - black/white pawn\n')

    def __move_command(self):
        source_x = self.__validate_coordinate(True)
        if source_x is None:
            return

        source_y = self.__validate_coordinate(False)
        if source_y is None:
            return

        destination_x = self.__validate_coordinate(True)
        if destination_x is None:
            return

        destination_y = self.__validate_coordinate(False)
        if destination_y is None:
            return

        moving_color = PieceColor.WHITE if self.__white_turn else PieceColor.BLACK
        self.__game_service.move(source_x, source_y, destination_x, destination_y, moving_color)
        self.__white_turn = not self.__white_turn
        print('Move performed successfully.')

    def __validate_coordinate(self, x_coordinate=True):
        coordinate_dictionary = {True: 'X', False: 'Y'}
        coordinate = input("Piece's {} coordinate: ".format(coordinate_dictionary[x_coordinate]))
        try:
            coordinate = int(coordinate)
            if coordinate < 0 or coordinate > 7:
                raise ValueError
        except ValueError:
            print('{} is not a valid {} coordinate. The coordinate must be a positive integer between 0 and 7.'.format(
                coordinate, coordinate_dictionary[x_coordinate]))
            return None
        return coordinate

    def run(self):
        running = True
        while running:
            try:
                self.__print_menu()
                self.__print_board()
                command = input('command > ')
                if command == 'exit':
                    running = False
                elif command in self.__commands:
                    self.__commands[command]()
                else:
                    print("'{}' is not a valid command.\n".format(command))
            except UserInputError as userInputError:
                print(str(userInputError) + '\n')
            except InvalidMoveError as invalidMoveError:
                print(str(invalidMoveError) + '\n')
            except Exception as exception:
                print('Unexpected exception occured: ' + str(exception) + '\n')
