import mysql.connector
import random
from card import Card
from config import get_db_config  # Importing the function

class Deck:
    def __init__(self, player_name):
        self.cards = self.load_cards_from_db(player_name)
        self.shuffle()

    def load_cards_from_db(self, player_name):
        # Connect to your MySQL database and fetch the normal monster cards
        db_config = get_db_config()
        db = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )

        cursor = db.cursor()

        query = "SELECT * FROM all_cards WHERE (frameType = 'normal' OR type = 'NormalMonster') ORDER BY RAND() LIMIT 10"

        cursor.execute(query)

        cards = cursor.fetchall()

        # Convert the tuples into Card objects
        cards = [Card(card[1], int(card[3]), card[12], int(card[7]), int(card[8])) for card in cards]

        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()