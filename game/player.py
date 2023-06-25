from deck import Deck
from field import Field
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = Deck()
        self.field = Field()
        self.graveyard = []

    def draw(self):
        if self.deck.cards:  # Check if the deck is not empty
            card = self.deck.draw_card()
            self.hand.append(card)
            print(f"{self.name} drew {card}")
            self.show_hand()
            if len(self.hand) > 7:  # Check if hand size exceeds 7
                self.discard()  # Discard a card
        else:
            print(f"{self.name}'s deck is empty. The game is over.")
            return False
        return True
    
    def discard(self):
        card = random.choice(self.hand)  # Choose a random card to discard
        self.hand.remove(card)  # Remove the card from the hand
        self.graveyard.append(card)  # Add the card to the graveyard
        print(f"{self.name} discarded {card} to the graveyard.")
        self.field.zones["graveyard"] = card  # Add the card to the player's graveyard zone on the field

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")
        print(f"{self.name} hand size is: {len(self.hand)}")
        print(f"{self.name} deck size is: {len(self.deck.cards)}")
        print(f"{self.name} graveyard size is: {len(self.graveyard)}")

    def choose_card_to_summon(self):
        print(f"{self.name}, choose a card to summon:")
        for card in self.hand:
            print(f"{card[1]}")  # Print the name of the card

        while True:  # Keep asking until a valid input is given
            choice = input("Enter the name of the card: ")
            for card in self.hand:
                if choice.lower() in card[1].lower():  # Check if the input is in the card name
                    return card

            print("Invalid input, please try again.")
    
    def summon(self):
        if not self.has_normal_summoned:
            summon_prompt = input(f"{self.name}, would you like to summon a monster? (yes/no): ")
            if summon_prompt.lower() != "yes":
                return
        else:
            print("You have already performed a Normal Summon this turn.")
            return

        # Ask the player to choose a summon type
        summon_type = input(f"{self.name}, would you like to perform a Normal Summon or a Tribute Summon? (normal/tribute): ")
        if summon_type.lower() not in ["normal", "tribute"]:
            print("Invalid summon type.")
            return

        # Ask the player to choose a card to summon
        print(f"{self.name}, choose a card to summon:")
        for i, card in enumerate(self.hand):
            print(f"{i}: {card.name}")
        card_index = int(input("Enter the number of the card: "))
        card = self.hand[card_index]

        # If the player chose to perform a Tribute Summon
        if summon_type.lower() == "tribute":
            # Check if the player has enough monsters to tribute
            monsters_on_field = [zone for zone in self.field.zones["main_monster_zones"] if zone is not None]
            if len(monsters_on_field) < card.summon_requirement:
                print("Not enough monsters on the field to tribute.")
                return

            # Ask the player to choose which monsters to tribute
            for _ in range(card.summon_requirement):
                print(f"{self.name}, choose a monster to tribute:")
                for i, monster in enumerate(monsters_on_field):
                    print(f"{i}: {monster.name}")
                monster_index = int(input("Enter the number of the monster: "))
                monster = monsters_on_field.pop(monster_index)
                self.field.zones["main_monster_zones"].remove(monster)
                self.graveyard.append(monster)

        # Remove the card from the player's hand
        self.hand.remove(card)

        # Ask the player to choose a position for the monster
        position = input("Enter the position for the monster ('attack', 'defense', or 'set'): ")
        card.set_position(position)

        # Move the card to one of the player's Main Monster Zones
        for zone in self.field.zones["main_monster_zones"]:
            if zone is None:
                zone = card
                break
        else:
            print("All Main Monster Zones are full.")

        self.has_normal_summoned = True
        card = self.choose_card_to_summon()
        self.field.place_card("player1", "main_monster_zones", card)
        self.can_summon = False

    
    def standby_phase(self):
        print(f"{self.name} is in the Standby Phase.")

    def draw_phase(self):
        print(f"{self.name} is in the Draw Phase.")
        return self.draw()

    def main_phase_1(self):
        print(f"{self.name} is in Main Phase 1.")
        self.can_summon = True

    def battle_phase(self):
        print(f"{self.name} is in the Battle Phase.")

    def main_phase_2(self):
        print(f"{self.name} is in Main Phase 2.")
        self.can_summon = True

    def end_phase(self):
        print(f"{self.name} is in the End Phase.")

    def get_hand_size(self):
        return len(self.hand)

    def get_deck_size(self):
        return len(self.deck.cards)
