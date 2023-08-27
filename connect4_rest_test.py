#!/usr/bin/env python
import unittest
import connect4
import re
import curses
from connect4_test import Connect4CLITestCase
import connect4_rest
import json

class TestConnect4RestClient(Connect4CLITestCase):

    def setUp(self) -> None:
        self.client = connect4_rest.app.test_client();

    def test_can_create_game_client(self):
        client = connect4_rest.Connect4Client()

    def test_can_create_game_client_using_flask_test_client(self):
        client = connect4_rest.Connect4Client(self.client)

    def test_user_can_start_a_game(self):
        client = connect4_rest.Connect4Client(self.client)
        game = client.createNewGame(user=1)
        self.assertIsNotNone(game.id)

    def test_starting_2_games_gives_different_ids(self):
        client = connect4_rest.Connect4Client(self.client)
        game_1 = client.createNewGame(user=1)
        game_2 = client.createNewGame(user=2)
        self.assertNotEqual(game_1.id, game_2.id)

    def test_can_create_anonymous_game(self):
        client = connect4_rest.Connect4Client(self.client)
        game = client.createNewGame()
        self.assertIsNotNone(game.id)

    def test_2_anonymous_games_have_different_ids(self):
        client = connect4_rest.Connect4Client(self.client)
        game_1 = client.createNewGame()
        game_2 = client.createNewGame()
        self.assertNotEqual(game_1.id, game_2.id)

    def test_can_get_player_key_upon_joining_game(self):
        client = connect4_rest.Connect4Client(self.client)
        game_1 = client.createNewGame()
        player = client.joinGame(game_1, user=1)
        self.assertEqual("red", player.color)

    def test_second_player_can_join_game(self):
        client = connect4_rest.Connect4Client(self.client)
        game_1 = client.createNewGame()
        player_1 = client.joinGame(game_1, user=1)
        player_2 = client.joinGame(game_1, user=2)
        self.assertEqual("black", player_2.color)

    def test_3rd_player_cant_join_game(self):
        client = connect4_rest.Connect4Client(self.client)
        game_1 = client.createNewGame()
        player_1 = client.joinGame(game_1, user=1)
        player_2 = client.joinGame(game_1, user=2)
        self.assertRaises(connect4_rest.GameFullException, lambda: client.joinGame(game_1, user=3))

    def test_player_cant_join_game_twice(self):
        client = connect4_rest.Connect4Client(self.client)
        game_1 = client.createNewGame()
        player_1 = client.joinGame(game_1, user=1)
        self.assertRaises(connect4_rest.AlreadyAPlayerException, lambda: client.joinGame(game_1, user=1))


if __name__ == "__main__":
    unittest.main()