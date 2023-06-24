from player import Player
from game import Game

# Now you can use these classes in your cardGame.py file
player1 = Player("Player 1")
player2 = Player("Player 2")

game = Game(player1, player2)
game.start()