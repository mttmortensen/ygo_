from flask import Flask, jsonify, request, render_template
from player import Player
from game import Game

app = Flask(__name__)

game = None

# Initialize game
player1 = Player("Player 1")
player2 = Player("Player 2")

# Front-End Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game  # Make sure to use the global game variable
    game = Game(player1, player2)
    game.start_game()  # This is a new method you'll need to add to your Game class
    return jsonify(game.get_state())

@app.route('/game_state', methods=['GET'])
def game_state():
    if game is None:
        return jsonify({"message": "The game hasn't started yet. Please start the game."})
    state = game.get_state()
    return jsonify(state)

@app.route('/perform_action', methods=['POST'])
def perform_action():
    # This is also a placeholder. You'll need to implement a method
    # to perform an action based on the request data.
    data = request.get_json()
    game.perform_action(data['action'])
    return jsonify(success=True)

# Error handling
@app.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)

