#!/usr/bin/env python
import unittest
import connect4

class TestConnect4(unittest.TestCase):

    def test_can_create_game(self):
        game = connect4.Game(6, 6)

    def test_can_create_token(self):
        game = connect4.Game(6, 6)
        token = game.token("red")

    def test_can_drop_token(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)

    def test_first_dropped_token_sinks_to_bottom(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        self.assertEqual(game.cellState(0, 0), "red")

    def test_can_drop_black_token(self):
        game = connect4.Game(6, 6)
        token = game.token("black")
        game.drop(token, 0)
        self.assertEqual(game.cellState(0, 0), "black")

    def test_can_drop_second_token_in_column(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        game.drop(token, 0)
        self.assertEqual(game.cellState(1, 0), "red")

    def test_first_dropped_token_doesnt_fill_second_row(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        self.assertEqual(game.cellState(1, 0), None)

    def test_cannot_drop_token_into_full_column(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        self.assertRaises(Exception, lambda: game.drop(token, 0))
    
    def test_game_not_over_after_3_drops(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        self.assertTrue(not game.over())

    def test_game_over_after_4_drops(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        game.drop(token, 0)
        self.assertTrue(game.over())

    def test_game_over_after_4_drops_side_by_side(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        game.drop(token, 0)
        game.drop(token, 1)
        game.drop(token, 2)
        game.drop(token, 3)
        self.assertTrue(game.over())

    def test_game_over_after_4_drops_with_different_colors(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        black_token = game.token("black")
        game.drop(token, 0)
        game.drop(black_token, 0)
        game.drop(token, 0)
        game.drop(black_token, 0)
        self.assertTrue(not game.over())

    def test_game_over_after_4_drops_with_different_colors_side_by_side(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        black_token = game.token("black")
        game.drop(token, 0)
        game.drop(black_token, 1)
        game.drop(token, 2)
        game.drop(black_token, 3)
        self.assertTrue(not game.over())

    def test_game_over_after_4_drops_diagonal_to_right(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        black_token = game.token("black")
        game.drop(token, 0)
        game.drop(black_token, 1)
        game.drop(token, 1)
        game.drop(black_token, 2)
        game.drop(black_token, 2)
        game.drop(token, 2)
        game.drop(black_token, 3)
        game.drop(black_token, 3)
        game.drop(black_token, 3)
        game.drop(token, 3)
        self.assertTrue(game.over())

    def test_game_over_after_4_drops_diagonal_to_left(self):
        game = connect4.Game(6, 6)
        token = game.token("red")
        black_token = game.token("black")
        game.drop(token, 3)
        game.drop(black_token, 2)
        game.drop(token, 2)
        game.drop(black_token, 1)
        game.drop(black_token, 1)
        game.drop(token, 1)
        game.drop(black_token, 0)
        game.drop(black_token, 0)
        game.drop(black_token, 0)
        game.drop(token, 0)
        self.assertTrue(game.over())


if __name__ == "__main__":
    unittest.main()