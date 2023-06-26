from player import Player
from game import Game
from deck import Deck

# Initialize game
deck1 = Deck()
deck1.load_cards_from_db()
player1 = Player("Player 1", deck1)

deck2 = Deck()
deck2.load_cards_from_db()
player2 = Player("Player 2", deck2)

game = Game(player1, player2)
game.start_game()