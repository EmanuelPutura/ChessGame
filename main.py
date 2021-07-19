"""
    @title: Quess - a chess game
    @author: Emanuel-Vasile Putura
    @date: 13.02.2021
"""
from presentation.console_ui.console import ConsoleUI
from presentation.gui.main_window import MainWindow
from services.game_service import GameService

if __name__ == "__main__":
    game_service = GameService()
    gui = MainWindow(game_service)
    gui.run()
    # consoleUI = ConsoleUI(game_service)
    # consoleUI.run()
