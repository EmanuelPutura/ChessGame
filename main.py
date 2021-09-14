"""
    @title: Quess - a chess game
    @author: Emanuel-Vasile Putura
    @date: 13.02.2021
"""
from infrastructure.database_repository import UsersDatabaseRepository
from presentation.console_ui.console import ConsoleUI
from presentation.gui.main_window import MainWindow
from services.game_service import GameService
from services.users_service import UsersService
from tests.test_piece_moving import TestPieceMoving

if __name__ == "__main__":
    TestPieceMoving().test_all()

    users_repository = UsersDatabaseRepository("databases/data.db")
    game_service = GameService()
    users_service = UsersService(users_repository)
    gui = MainWindow(game_service, users_service)
    gui.run()
    # consoleUI = ConsoleUI(game_service)
    # consoleUI.run()
