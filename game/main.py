from player import Player
from game import Game
from deck import Deck

# Initialize game
deck1 = Deck("Player 1")
deck1.load_cards_from_db("Player 1")
player1 = Player("Player 1", deck1)

deck2 = Deck("Player 2")
deck2.load_cards_from_db("Player 2")
player2 = Player("Player 2", deck2)

game = Game(player1, player2)
game.start_game()