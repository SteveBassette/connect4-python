from flask import Flask, jsonify, request
import uuid
from pprint import pprint as print
import json

app = Flask(__name__)

# player_list = {"1": ['red', 'black']}
games = dict()

class NetworkGame():
    def __init__(self, id):
        self.id = id

class NetworkPlayer():
    def __init__(self, color):
        self.color = color

class Connect4Client():

    def __init__(self, client=None):
        self.client = client

    def createNewGame(self, user=None):
        new_game_response = self.client.get("/game/new")
        new_game_data = json.loads(new_game_response.data)
        return NetworkGame(new_game_data['game_id'])

    def joinGame(self, game, user):
        join_response = self.client.get("/join/" + game.id)
        join_data = json.loads(join_response.data)
        return NetworkPlayer(join_data['player_key'])


@app.route("/game/new", methods=['POST', 'GET'])
def new_game():
    user_id = request.form.get("user_id", "anonymous")
    game_id = uuid.uuid1()
    games[str(game_id)] = {
        "player_list": ['red', 'black'],
        "player_assignments": [],
        "owner": user_id
    }
    return jsonify({"game_id":game_id})

@app.route("/status/1")
def game_status():
    return jsonify({"game_id":"1"})

@app.route("/join/<game_id>")
def join_game(game_id):
    token = 'red'
    token = games[game_id]["player_list"][len(games[game_id]["player_assignments"])]
    games[game_id]["player_assignments"].append("anonymous")
    return jsonify({"player_key":token})

if __name__ == "__main__":
    client = app.test_client();
    response = client.get("/game/new")
    print(response)