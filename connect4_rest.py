import flask
from flask import Flask, jsonify, request
import uuid
from pprint import pprint as print

app = Flask(__name__)

# player_list = {"1": ['red', 'black']}
games = dict()

class GameFullException(Exception):
    """This exception indicates the Game has reached its player capacity"""
    pass

class AlreadyAPlayerException(Exception):
    """This exception indicates the Game has reached its player capacity"""
    pass

class NetworkGame():
    """A NetworkGame is a game hosted by a server and played by multiple
    players on different clients"""

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
        new_game_data = new_game_response.json()
        return NetworkGame(new_game_data['game_id'])

    def joinGame(self, game, user=None):
        if user:
            response = self.client.post("/join/" + game.id, json={"user_id":user})
        else:
            response = self.client.get("/join/" + game.id)

        try:
            join_data = response.json()
        except:
            raise Exception()
            
        if  response.status_code == 200:
            return NetworkPlayer(join_data['player_key'])

        elif response.status_code == 409 and join_data['code'] == 'g1':
            raise GameFullException()

        elif response.status_code == 409 and join_data['code'] == 'g2':
            raise AlreadyAPlayerException()

        else:
            raise Exception()


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

@app.route("/join/<game_id>", methods=['POST', 'GET'])
def join_game(game_id):
    user_id = request.form.get("user_id", "anonymous")

    if len(games[game_id]["player_assignments"]) >= len(games[game_id]["player_list"]):
        return jsonify(error=409, code='g1', text="Game is full"), 409
    
    elif not user_id == 'anonymous' and user_id in games[game_id]["player_assignments"]:
        return jsonify(error=409, code="g2", text="User is already playing the game"), 409
    
    else:
        token = games[game_id]["player_list"][len(games[game_id]["player_assignments"])]
        games[game_id]["player_assignments"].append(user_id)
        return jsonify({"player_key":token})

if __name__ == "__main__":
    client = app.test_client();
    response = client.get("/game/new")
    print(response)