import mysql.connector
import random
from card import Card
from config import get_db_config  # Importing the function

class Deck:
    def __init__(self):
        self.cards = self.load_cards_from_db()
        self.shuffle()

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
        
        # This is just for testing. I will uncomment below once done. 
        # First, select one monster of level 5 or higher
        query_high_level = "SELECT * FROM all_cards WHERE (frameType = 'normal' OR type = 'NormalMonster') AND level >= 5 LIMIT 1"
        cursor.execute(query_high_level)
        high_level_card = cursor.fetchone()

        # Then, select up to 9 other normal monsters of any level
        query_other_cards = "SELECT * FROM all_cards WHERE frameType = 'normal' OR type = 'NormalMonster' AND name != %s LIMIT 9"
        cursor.execute(query_other_cards, (high_level_card[1],))
        other_cards = cursor.fetchall()

        # Combine the two sets of cards
        other_cards = [Card(high_level_card[1], int(high_level_card[3]), high_level_card[12], int(high_level_card[7]), int(high_level_card[8]))] + \
                      [Card(card[1], int(card[3]), card[12], int(card[7]), int(card[8])) for card in other_cards]

        return other_cards

        #cursor = db.cursor()

        #query = "SELECT * FROM all_cards WHERE frameType = 'normal' LIMIT 10"

        #cursor.execute(query)

        #cards = cursor.fetchall()

        # Convert the tuples into Card objects
        #cards = [Card(card[1], int(card[3]), card[12], int(card[7]), int(card[8])) for card in cards]

        #return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()