"""
    @title: Quess - a chess game
    @author: Emanuel-Vasile Putura
    @date: 13.02.2021
"""
from presentation.console_ui.console import ConsoleUI
from presentation.gui.main_window import MainWindow
from services.game_service import GameService

if __name__ == "__main__":
    # gui = MainWindow()
    # gui.run()
    game_service = GameService()
    consoleUI = ConsoleUI(game_service)
    consoleUI.run()
