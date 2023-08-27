#!/usr/bin/env python
import unittest
import connect4
import re
import curses
from connect4_test import Connect4CLITestCase
import connect4_rest
import json

class TestConnect4Rest(Connect4CLITestCase):

    def setUp(self) -> None:
        # self.app = create_app()
        # self.app.config.update({
        #     "TESTING": True,
        # })
        self.client = connect4_rest.app.test_client();

    def test_can_get_game_status(self):
        response = self.client.get("/status/1")
        data = json.loads(response.data)

    def test_can_start_a_game(self):
        response = self.client.post("/game/new", data={"user_id": 1})
        # response = self.client.post("/game/new")
        # data = json.loads(response.data)

    def test_starting_a_game_gives_game_id(self):
        response = self.client.post("/game/new", data={"user_id": 1})
        data = json.loads(response.data)
        self.assertIsNotNone(data["game_id"])

    def test_starting_2_games_gives_different_ids(self):
        game_1_response = self.client.post("/game/new", data={"user_id": 1})
        game_1_data = json.loads(game_1_response.data)
        game_2_response = self.client.post("/game/new", data={"user_id": 1})
        game_2_data = json.loads(game_2_response.data)
        self.assertNotEqual(game_1_data["game_id"], game_2_data["game_id"])

    def test_can_create_anonymous_game(self):
        game_1_response = self.client.get("/game/new")
        game_1_data = json.loads(game_1_response.data)
        self.assertIsNotNone(game_1_data["game_id"])
        # self.assertNotEqual(game_1_data["game_id"], game_2_data["game_id"])

    def test_2_anonymous_games_have_different_ids(self):
        game_1_response = self.client.get("/game/new")
        game_1_data = json.loads(game_1_response.data)
        game_2_response = self.client.get("/game/new")
        game_2_data = json.loads(game_2_response.data)
        self.assertNotEqual(game_1_data["game_id"], game_2_data["game_id"])

    def test_can_join_a_game(self):
        game_1_response = self.client.get("/game/new")
        game_1_data = json.loads(game_1_response.data)
        response = self.client.get("/join/"+game_1_data["game_id"])

    def test_can_get_player_key_upon_joining_game(self):
        game_1_response = self.client.get("/game/new")
        game_1_data = json.loads(game_1_response.data)
        response = self.client.get("/join/" + game_1_data["game_id"])
        data = json.loads(response.data)
        self.assertEqual("red", data['player_key'])

    def test_second_player_can_join_game(self):
        game_1_response = self.client.get("/game/new")
        game_1_data = json.loads(game_1_response.data)
        player_1_response = self.client.get("/join/" + game_1_data["game_id"])
        player_2_response = self.client.get("/join/" + game_1_data["game_id"])
        player_2 = json.loads(player_2_response.data)
        self.assertEqual("black", player_2['player_key'])


if __name__ == "__main__":
    unittest.main()