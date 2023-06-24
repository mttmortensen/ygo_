import mysql.connector
from ..config import get_db_config  # Importing the function
import random

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

        query = "SELECT * FROM all_cards WHERE frameType = 'normal' LIMIT 7"

        cursor.execute(query)

        cards = cursor.fetchall()

        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()