from flask import Flask, jsonify, request, render_template
from player import Player
from game import Game

app = Flask(__name__)

# Initialize game
player1 = Player("Player 1")
player2 = Player("Player 2")
game = Game(player1, player2)

# Front-End Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state', methods=['GET'])
def game_state():
    # Check if the game has started
    if game.current_phase is None:
        return jsonify({"message":"The game hasn't started. Please start it or refresh the browser."})
    # This is just a placeholder. You'll need to implement a method
    # to get the current game state as a JSON-serializable dictionary.
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

# Not using for now
# game.start()