import unittest
from application.server import Moves, Server
from unittest.mock import patch


class TestMoves(unittest.TestCase):
    def test_add_move(self):
        moves = Moves(max_length=3)
        moves.add_move('rock', 'paper')
        self.assertEqual(moves.get_all_moves(), [['rock', 'paper']])

        moves.add_move('scissors', 'rock')
        moves.add_move('paper', 'scissors')
        self.assertEqual(moves.get_all_moves(), [['rock', 'paper'], ['scissors', 'rock'], ['paper', 'scissors']])

    def test_add_move_overflow(self):
        moves = Moves(max_length=3)
        moves.add_move('rock', 'paper')
        moves.add_move('scissors', 'rock')
        moves.add_move('paper', 'scissors')
        moves.add_move('rock', 'rock')
        self.assertEqual(moves.get_all_moves(), [['scissors', 'rock'], ['paper', 'scissors'], ['rock', 'rock']])

    def test_get_last_move(self):
        moves = Moves(max_length=3)
        moves.add_move('rock', 'paper')
        self.assertEqual(moves.get_last_move(), ['rock', 'paper'])

        moves.add_move('scissors', 'rock')
        self.assertEqual(moves.get_last_move(), ['scissors', 'rock'])

    def test_get_all_moves(self):
        moves = Moves(max_length=3)
        moves.add_move('rock', 'paper')
        moves.add_move('scissors', 'rock')
        self.assertEqual(moves.get_all_moves(), [['rock', 'paper'], ['scissors', 'rock']])

        moves.add_move('paper', 'scissors')
        self.assertEqual(moves.get_all_moves(), [['rock', 'paper'], ['scissors', 'rock'], ['paper', 'scissors']])

    def test_repr(self):
        moves = Moves(max_length=3)
        moves.add_move('rock', 'paper')
        moves.add_move('scissors', 'rock')
        self.assertEqual(repr(moves), "['rock', 'paper'] <-> ['scissors', 'rock']")

        moves.add_move('paper', 'scissors')
        self.assertEqual(repr(moves), "['rock', 'paper'] <-> ['scissors', 'rock'] <-> ['paper', 'scissors']")


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

    def test_get_win_of(self):
        self.assertEqual(self.server.get_win_of('rock'), 'paper')
        self.assertEqual(self.server.get_win_of('scissors'), 'rock')
        self.assertEqual(self.server.get_win_of('paper'), 'scissors')

    def test_get_less_common_user_move_no_moves(self):
        with patch('random.choice', return_value='rock'):
            self.assertEqual(self.server.get_less_common_user_move(), 'rock')

    def test_get_less_common_user_move_with_moves(self):
        self.server.moves.add_move('rock', 'scissors')
        self.server.moves.add_move('paper', 'rock')
        self.server.moves.add_move('scissors', 'paper')
        self.server.moves.add_move('rock', 'rock')
        self.assertEqual(self.server.get_less_common_user_move(), 'paper')

    def test_make_move_first_move(self):
        with patch('random.choice', return_value='rock'):
            self.server.make_move('paper')
            last_move = self.server.moves.get_last_move()
            self.assertEqual(last_move, ['paper', 'rock'])

    def test_make_move_user_wins(self):
        self.server.rounds.append(0)
        self.server.moves.add_move('scissors', 'paper')
        with patch('random.randint', return_value=3):
            self.server.make_move('scissors')
            last_move = self.server.moves.get_last_move()
            self.assertEqual(last_move, ['scissors', 'rock'])

    def test_make_move_computer_wins(self):
        self.server.rounds.append(1)
        self.server.moves.add_move('rock', 'paper')
        with patch('random.randint', return_value=3):
            self.server.make_move('paper')
            last_move = self.server.moves.get_last_move()
            self.assertEqual(last_move, ['paper', 'scissors'])

    def test_make_move_draw(self):
        self.server.rounds.append(2)
        self.server.moves.add_move('rock', 'rock')
        with patch('random.randint', return_value=3):
            with patch('random.choice', return_value='rock'):
                self.server.make_move('rock')
                last_move = self.server.moves.get_last_move()
                self.assertEqual(last_move, ['rock', 'rock'])

    def test_get_result_user_wins(self):
        self.server.moves.add_move('scissors', 'rock')
        self.server.get_result()
        self.assertEqual(self.server.rounds[-1], 1)

    def test_get_result_computer_wins(self):
        self.server.moves.add_move('rock', 'paper')
        with patch('builtins.print') as mock_print:
            self.server.get_result()
        self.assertEqual(self.server.result[1], 1)
        self.assertIn(1, self.server.rounds)

    def test_get_result_draw(self):
        self.server.moves.add_move('rock', 'rock')
        with patch('builtins.print') as mock_print:
            self.server.get_result()
        self.assertEqual(self.server.result[2], 1)
        self.assertIn(2, self.server.rounds)


if __name__ == '__main__':
    unittest.main()
