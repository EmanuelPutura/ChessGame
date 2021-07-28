import unittest

from chess_pieces.bishop import Bishop
from chess_pieces.king import King
from chess_pieces.knight import Knight
from chess_pieces.pawn import Pawn
from chess_pieces.queen import Queen
from chess_pieces.rook import Rook
from errors.exceptions import InvalidMoveError
from presentation.gui.main_window import MainWindow
from services.game_service import GameService
from tools.constants import PieceColor


class TestPieceMoving(unittest.TestCase):
    def setUp(self):
        self.__game_service = GameService()

    def test_all(self):
        self.test_basic_movement()
        self.test_check_situations()

    def test_basic_movement(self):
        self.setUp()
        board = self.__game_service.board

        # move the left black knight - should work
        self.__game_service.move(0, 1, 2, 0, PieceColor.BLACK)
        self.assertEqual(board[0, 1], None)
        self.assertEqual(board[2, 0], Knight(board, 2, 0, PieceColor.BLACK))

        # attempt to move the left black knight on a cell occupied by a black piece - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 2, 0, 1, 2, PieceColor.BLACK)
        try:
            self.__game_service.move(2, 0, 1, 2, PieceColor.BLACK)
        except InvalidMoveError as invalidMoveError:
            self.assertEqual(str(invalidMoveError), 'InvalidMoveError: Cannot move to (1, 2) cell.')

        # attempt to simply move a pawn - should work
        self.__game_service.move(1, 1, 2, 1, PieceColor.BLACK)
        self.assertEqual(board[1, 1], None)
        self.assertEqual(board[2, 1], Pawn(board, 2, 1, PieceColor.BLACK))

        # attempt to double-move an already moved pawn - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 2, 1, 4, 1, PieceColor.BLACK)

        # attempt to double-move a pawn - should work
        self.__game_service.move(1, 2, 3, 2, PieceColor.BLACK)
        self.assertEqual(board[1, 2], None)
        self.assertEqual(board[3, 2], Pawn(board, 3, 2, PieceColor.BLACK))

        # attempt to attack-move a black pawn on a cell occupied by a black piece - should work
        self.assertRaises(InvalidMoveError, self.__game_service.move, 2, 1, 3, 2, PieceColor.BLACK)

        # attempt to move the left black rook - should work
        self.__game_service.move(0, 0, 0, 1, PieceColor.BLACK)
        self.assertEqual(board[0, 0], None)
        self.assertEqual(board[0, 1], Rook(board, 0, 1, PieceColor.BLACK))

        # attempt to move a white pawn by 2 cells - should work
        self.__game_service.move(6, 3, 4, 3, PieceColor.WHITE)
        self.assertEqual(board[6, 3], None)
        self.assertEqual(board[4, 3], Pawn(board, 4, 3, PieceColor.WHITE))

        # attempt to capture a white pawn with a black pawn - should work
        self.__game_service.move(3, 2, 4, 3, PieceColor.BLACK)
        self.assertEqual(board[3, 2], None)
        self.assertEqual(board[4, 3], Pawn(board, 4, 3, PieceColor.BLACK))

        # attempt to move the white queen - should work
        self.__game_service.move(7, 3, 5, 3, PieceColor.WHITE)
        self.assertEqual(board[7, 3], None)
        self.assertEqual(board[5, 3], Queen(board, 5, 3, PieceColor.WHITE))

        # attempt to move a black pawn on a cell occupied by the white queen - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 4, 3, 5, 3, PieceColor.BLACK)

        # attempt to diagonally move the white queen, involving also a capture - should work
        self.__game_service.move(5, 3, 2, 0, PieceColor.WHITE)
        self.assertEqual(board[5, 3], None)
        self.assertEqual(board[2, 0], Queen(board, 2, 0, PieceColor.WHITE))

        # attempt to move the black bishop - should work
        self.__game_service.move(0, 2, 1, 1, PieceColor.BLACK)
        self.assertEqual(board[0, 2], None)
        self.assertEqual(board[1, 1], Bishop(board, 1, 1, PieceColor.BLACK))

        # attempt to move the black bishop, involving a capture - should work
        self.__game_service.move(1, 1, 6, 6, PieceColor.BLACK)
        self.assertEqual(board[1, 1], None)
        self.assertEqual(board[6, 6], Bishop(board, 6, 6, PieceColor.BLACK))

        # attempt to move the white queen - should work
        self.__game_service.move(2, 0, 4, 2, PieceColor.WHITE)
        self.assertEqual(board[2, 0], None)
        self.assertEqual(board[4, 2], Queen(board, 4, 2, PieceColor.WHITE))

        # attempt to move the white queen through a cell already occupied by a black piece - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 4, 2, 0, 6, PieceColor.WHITE)

        # attempt to move the white queen through a cell already occupied by a white piece - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 4, 2, 7, 5, PieceColor.WHITE)

        # attempt to move the white queen - should work
        self.__game_service.move(4, 2, 5, 1, PieceColor.WHITE)
        self.assertEqual(board[4, 2], None)
        self.assertEqual(board[5, 1], Queen(board, 5, 1, PieceColor.WHITE))

        # attempt to move the white queen, involving a capture - should work
        self.__game_service.move(5, 1, 2, 1, PieceColor.WHITE)
        self.assertEqual(board[5, 1], None)
        self.assertEqual(board[2, 1], Queen(board, 2, 1, PieceColor.WHITE))

        # attempt to move the black rook through a cell already occupied by a white piece - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 0, 1, 4, 1, PieceColor.BLACK)

        # attempt to move the black rook, involving a capture - should work
        self.__game_service.move(0, 1, 2, 1, PieceColor.BLACK)
        self.assertEqual(board[0, 1], None)
        self.assertEqual(board[2, 1], Rook(board, 2, 1, PieceColor.BLACK))

        # attempt to move the black rook, involving a capture - should work
        self.__game_service.move(2, 1, 6, 1, PieceColor.BLACK)
        self.assertEqual(board[2, 1], None)
        self.assertEqual(board[6, 1], Rook(board, 6, 1, PieceColor.BLACK))

        # attempt to move the white knight - should work
        self.__game_service.move(7, 6, 5, 5, PieceColor.WHITE)
        self.assertEqual(board[7, 6], None)
        self.assertEqual(board[5, 5], Knight(board, 5, 5, PieceColor.WHITE))

        # attempt to move the white knight - should work
        self.__game_service.move(5, 5, 3, 4, PieceColor.WHITE)
        self.assertEqual(board[5, 5], None)
        self.assertEqual(board[3, 4], Knight(board, 3, 4, PieceColor.WHITE))

        # attempt to move the white knight, involving a capture - should work
        self.__game_service.move(3, 4, 1, 5, PieceColor.WHITE)
        self.assertEqual(board[3, 4], None)
        self.assertEqual(board[1, 5], Knight(board, 1, 5, PieceColor.WHITE))

        # attempt to diagonally move the white king, should work
        self.__game_service.move(7, 4, 6, 3, PieceColor.WHITE)
        self.assertEqual(board[7, 4], None)
        self.assertEqual(board[6, 3], King(board, 6, 3, PieceColor.WHITE))

        # attempt to move the white king, should work
        self.__game_service.move(6, 3, 5, 3, PieceColor.WHITE)
        self.assertEqual(board[6, 3], None)
        self.assertEqual(board[5, 3], King(board, 5, 3, PieceColor.WHITE))

        # attempt to move the black queen - should work
        self.__game_service.move(0, 3, 1, 2, PieceColor.BLACK)
        self.assertEqual(board[0, 3], None)
        self.assertEqual(board[1, 2], Queen(board, 1, 2, PieceColor.BLACK))

        # attempt to move the black queen - should work
        self.__game_service.move(1, 2, 4, 2, PieceColor.BLACK)
        self.assertEqual(board[1, 2], None)
        self.assertEqual(board[4, 2], Queen(board, 4, 2, PieceColor.BLACK))

        # attempt to move the white king while in chess - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 5, 3, 4, 3, PieceColor.WHITE)

        # attempt to move the white king, involving a capture - should work
        self.__game_service.move(5, 3, 4, 2, PieceColor.WHITE)
        self.assertEqual(board[5, 3], None)
        self.assertEqual(board[4, 2], King(board, 4, 2, PieceColor.WHITE))

        # attempt to move the king over two cells - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 4, 2, 2, 2, PieceColor.WHITE)

        # attempt to move the white king, involving entering in check - should fail
        self.assertRaises(InvalidMoveError, self.__game_service.move, 4, 2, 5, 2, PieceColor.WHITE)

        # attempt to move the white horse - should work
        self.__game_service.move(1, 5, 2, 7, PieceColor.WHITE)
        self.assertEqual(board[1, 5], None)
        self.assertEqual(board[2, 7], Knight(board, 2, 7, PieceColor.WHITE))

        # attempt to move the black rook - should work
        self.__game_service.move(6, 1, 0, 1, PieceColor.BLACK)
        self.assertEqual(board[6, 1], None)
        self.assertEqual(board[0, 1], Rook(board, 0, 1, PieceColor.BLACK))

        # attempt to move the white horse - should work
        self.__game_service.move(7, 1, 5, 2, PieceColor.WHITE)
        self.assertEqual(board[7, 1], None)
        self.assertEqual(board[5, 2], Knight(board, 5, 2, PieceColor.WHITE))

        # attempt to move the white rook - should work
        self.__game_service.move(7, 0, 7, 1, PieceColor.WHITE)
        self.assertEqual(board[7, 0], None)
        self.assertEqual(board[7, 1], Rook(board, 7, 1, PieceColor.WHITE))

        # attempt to move the black knight - should work
        self.__game_service.move(0, 6, 2, 5, PieceColor.BLACK)
        self.assertEqual(board[0, 6], None)
        self.assertEqual(board[2, 5], Knight(board, 2, 5, PieceColor.BLACK))

        # attempt to move the black knight - should work
        self.__game_service.move(2, 5, 3, 3, PieceColor.BLACK)
        self.assertEqual(board[2, 5], None)
        self.assertEqual(board[3, 3], Knight(board, 3, 3, PieceColor.BLACK))

        # attempt to move the white rook - should work
        self.__game_service.move(7, 1, 1, 1, PieceColor.WHITE)
        self.assertEqual(board[7, 1], None)
        self.assertEqual(board[1, 1], Rook(board, 1, 1, PieceColor.WHITE))

        # attempt to move the black knight - should work
        self.__game_service.move(3, 3, 2, 1, PieceColor.BLACK)
        self.assertEqual(board[3, 3], None)
        self.assertEqual(board[2, 1], Knight(board, 2, 1, PieceColor.BLACK))

        # attempt to move the white king, involving a capture - should work
        self.__game_service.move(4, 2, 3, 2, PieceColor.WHITE)
        self.assertEqual(board[4, 2], None)
        self.assertEqual(board[3, 2], King(board, 3, 2, PieceColor.WHITE))

        # attempt to move the black knight - should work
        self.__game_service.move(2, 1, 0, 2, PieceColor.BLACK)
        self.assertEqual(board[2, 1], None)
        self.assertEqual(board[0, 2], Knight(board, 0, 2, PieceColor.BLACK))

    def test_check_situations(self):
        board = self.__game_service.board

        # attempt to move a black pawn - should work (now white king is in check)
        self.__game_service.move(1, 3, 2, 3, PieceColor.BLACK)
        self.assertEqual(board[1, 3], None)
        self.assertEqual(board[2, 3], Pawn(board, 2, 3, PieceColor.BLACK))

        # because the king is in check the next white move must get the king out of check (else checkmate). In this case, only the king can move
        for piece in self.__game_service.board.whites:
            if piece.__class__.__name__ != "King" and piece.get_move_options() != []:
                assert False

        # the moves that the king can do in this situation
        king = board[3, 2]
        king_moves = king.get_move_options()
        assert(len(king_moves) == 6)

        moves = [(2, 2), (3, 3), (4, 3), (4, 2), (4, 1), (3, 1)]
        for move in moves:
            assert(move in king_moves)

        # the white rook (and the other pieces but for the king too) cannot move in this situation (because of the check)
        self.assertRaises(InvalidMoveError, self.__game_service.move, 1, 1, 1, 2, PieceColor.WHITE)

        # move the white king
        self.__game_service.move(3, 2, 4, 2, PieceColor.WHITE)

        # move the black pawn in order to produce again check
        self.__game_service.move(2, 3, 3, 3, PieceColor.BLACK)

        # now the white knight should have only one possible move, capturing the black pawn who produced the check
        assert(board[5, 2].get_move_options() == [(3, 3)])

        # all the other pieces (but for the white knight and the king) should not be able to move
        for piece in self.__game_service.board.whites:
            if piece.__class__.__name__ != "King" and piece.get_move_options() != []:
                if not piece.x == 5 or not piece.y == 2:
                    assert False

        gui = MainWindow(self.__game_service)
        gui.run()

        # TODO: move the pawn until the end of the table and take a new black piece
        # TODO: test check cases
