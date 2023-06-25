import mysql.connector
import random
from card import Card
from config import get_db_config  # Importing the function

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

        query = "SELECT * FROM all_cards WHERE frameType = 'normal' LIMIT 10"

        cursor.execute(query)

        cards = cursor.fetchall()

        # Create Card instances for each card
        card_objects = []
        for card in cards:
            card_name = card[1]
            card_level = int(card[3]) if card[3] is not None else None
            card_type = card[12]
            card_object = Card(card_name, card_level, card_type)
            card_objects.append(card_object)

        return card_objects

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()