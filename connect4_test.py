#!/usr/bin/env python
import unittest
import connect4
import re

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


class TestScreenDummy(unittest.TestCase):

    def test_can_create_a_screen(self):
        test_screen = connect4.Screen()

    def test_can_specify_screen_size(self):
        test_screen = connect4.Screen(width=10, height=10)

    def test_cannot_add_string_to_screen_outside_width(self):
        test_screen = connect4.Screen(width=1, height=1)
        self.assertRaises(Exception, lambda: test_screen.addstr(0, 1, '.'))

    def test_cannot_add_string_to_screen_outside_height(self):
        test_screen = connect4.Screen(width=1, height=1)
        self.assertRaises(Exception, lambda: test_screen.addstr(1, 0, '.'))

    def test_can_specify_empty_screen_character(self):
        test_screen = connect4.Screen(width=1, height=1, background='#')
        self.assertEqual(str(test_screen), '#')

    def test_can_get_string_added_to_screen(self):
        test_screen = connect4.Screen()
        test_screen.addstr(0, 0, '.')
        self.assertEqual(str(test_screen), '.')

    def test_can_add_string_to_second_character_on_screen(self):
        test_screen = connect4.Screen(2,2,background='#')
        test_screen.addstr(0, 1, '.')
        self.assertEqual(str(test_screen), '#.\n##')

    def test_can_add_string_to_second_row_on_screen(self):
        test_screen = connect4.Screen(2,2,background='#')
        test_screen.addstr(1, 0, '.')
        self.assertEqual(str(test_screen), '##\n.#')

    def test_can_clear_the_screen(self):
        test_screen = connect4.Screen(2,2,background='#')
        test_screen.addstr(1, 0, '.')
        test_screen.clear()
        self.assertEqual(str(test_screen), '##\n##')

    def test_can_write_multiple_chars(self):
        test_screen = connect4.Screen(5,2,background='#')
        test_screen.addstr(0, 0, '123')
        self.assertEqual(str(test_screen), '123##\n#####')

    def test_can_refresh(self):
        test_screen = connect4.Screen(5,2,background='#')
        try:
            test_screen.refresh
        except:
            self.fail("Couldn't refresh the page")

class TestConnect4CLI(unittest.TestCase):

    def assertScreenEquals(self, screen, expected):
        
        self.assertEqual(str(screen), re.sub("(^ *)|(\n^ *$)", "", expected[1:], flags=re.MULTILINE))
        # self.assertEqual(str(screen), expected[1:].replace(" ", ""))

    def test_can_pass_cligame_a_screen(self):
        test_screen = connect4.Screen()
        game = connect4.TestedCliGame(test_screen)

    def test_cligame_empty_board_pixelcomparison(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         v#####
                         ______
                         ######
                         ######
                         ######
                         ######
                         ######
                         ######
                         ~~~~~~""")

    def test_cligame_dropped_token_pixelcomparison(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.drop()
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         v#####
                         ______
                         ######
                         ######
                         ######
                         ######
                         ######
                         r#####
                         ~~~~~~""")

    def test_cligame_2_dropped_token_pixelcomparison(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.drop()
        game.drop()
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         v#####
                         ______
                         ######
                         ######
                         ######
                         ######
                         b#####
                         r#####
                         ~~~~~~""")

    def test_cligame_can_shift_right(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.shiftRight()
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         #v####
                         ______
                         ######
                         ######
                         ######
                         ######
                         ######
                         ######
                         ~~~~~~""")

    def test_cligame_cant_shift_right_past_screen(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.shiftRight()
        game.shiftRight()
        game.shiftRight()
        game.shiftRight()
        game.shiftRight()
        game.shiftRight()
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         #####v
                         ______
                         ######
                         ######
                         ######
                         ######
                         ######
                         ######
                         ~~~~~~""")

    def test_cligame_can_shift_left(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.shiftRight()
        game.shiftLeft()
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         v#####
                         ______
                         ######
                         ######
                         ######
                         ######
                         ######
                         ######
                         ~~~~~~""")

    def test_cligame_cant_shift_left_past_screen(self):
        test_screen = connect4.Screen(width=6, height=9, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.shiftLeft()
        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                         v#####
                         ______
                         ######
                         ######
                         ######
                         ######
                         ######
                         ######
                         ~~~~~~""")

    def test_cligame_print_game_over_after_game_finishes(self):
        test_screen = connect4.Screen(width=20, height=14, background='#')
        game = connect4.TestedCliGame(test_screen)
        game.drop()
        game.drop()
        game.shiftRight()

        game.drop()
        game.drop()
        game.shiftRight()

        game.drop()
        game.drop()
        game.shiftRight()

        game.drop()

        game.paintGameBoard()
        self.assertScreenEquals(test_screen, """
                                ###v################
                                ______##############
                                ####################
                                ####################
                                ####################
                                ####################
                                bbb#################
                                rrrr################
                                ~~~~~~##############
                                ####################
                                GAME OVER ...#######
                                Press:##############
                                ####r) restart######
                                ####q) quit#########
                                """)

if __name__ == "__main__":
    unittest.main()