import random
import mysql.connector
from config import get_db_config  # Importing the function

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        if deck.cards:  # Check if the deck is not empty
            card = deck.draw_card()
            self.hand.append(card)
            print(f"{self.name} drew {card}")
            self.show_hand()
        else:
            print("The deck is empty. The game is over.")
            return False
        return True

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")

class Deck:
    def __init__(self):
        self.cards = self.load_cards_from_db()

    def load_cards_from_db(self):
        # Connect to your MySQL database and fetch the normal monster cards
        db_config = get_db_config()
        db = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

        cursor = db.cursor()

        query = "SELECT * FROM all_cards WHERE frameType = 'normal' LIMIT 6"

        cursor.execute(query)

        cards = cursor.fetchall()

        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.deck = Deck()
        self.deck.shuffle()

    def start(self):
        # Each player draws 3 cards
        for _ in range(3):
            for player in self.players:
                player.draw(self.deck)

        # Game continues until deck is empty
        while self.deck.cards:
            for player in self.players:
                if not player.draw(self.deck):  # If the deck is empty, end the game
                    return

# Initialize players
player1 = Player("Player 1")
player2 = Player("Player 2")

# Initialize and start game
game = Game(player1, player2)
game.start()
