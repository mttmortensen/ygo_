from player import Player
from game import Game
from deck import Deck

# Initialize game
deck1 = Deck()
deck1.load_cards_from_db()
deck1.shuffle()

deck2 = Deck()
deck2.load_cards_from_db()
deck2.shuffle()

game = Game()  # Create the game first

player1 = Player(game, "Player 1", deck1)  # Pass the game to the players
player2 = Player(game, "Player 2", deck2)

game.players = [player1, player2]  # Update the game's players

game.start_game()