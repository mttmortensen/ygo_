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
            print(f"{self.name}'s deck is empty. The game is over.")
            return False
        return True

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")
    
    def standby_phase(self):
        print(f"{self.name} is in the Standby Phase.")

    def draw_phase(self):
        print(f"{self.name} is in the Draw Phase.")
        return self.draw()

    def main_phase_1(self):
        print(f"{self.name} is in Main Phase 1.")

    def battle_phase(self):
        print(f"{self.name} is in the Battle Phase.")

    def main_phase_2(self):
        print(f"{self.name} is in Main Phase 2.")

    def end_phase(self):
        print(f"{self.name} is in the End Phase.")

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
        # Each player draws 5 cards
        for _ in range(5):
            for player in self.players:
                print(f"It's {player.name}'s turn.")
                if not player.draw(self.deck):  # If the deck is empty, end the game
                    return

        # Game continues until a player's deck is empty
        while True:
            for player in self.players:
                print(f"It's {player.name}'s turn.")
                player.standby_phase()
                if not player.draw_phase():  # If the deck is empty, end the game
                    return
                player.main_phase_1()
                player.battle_phase()
                player.main_phase_2()
                player.end_phase()

# Initialize players
player1 = Player("Player 1")
player2 = Player("Player 2")

# Initialize and start game
game = Game(player1, player2)
game.start()