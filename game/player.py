from deck import Deck
from field import Field
import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = Deck()
        self.graveyard = []
        self.field = Field(self.name)
        self.has_normal_summoned = False
        self.can_summon = True

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
        while True:
            print("Choose a monster to summon:")
            for i, card in enumerate(self.hand):
                print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
            card_index = input("Enter the number of the card: ")
            if card_index.isdigit() and int(card_index) in range(len(self.hand)):
                return self.hand[int(card_index)]
            else:
                print("Invalid input. Please enter a valid number.")
    
    def summon(self):
        if self.has_normal_summoned:
            print("You have already performed a Normal Summon this turn.")
            return

        # Ask the player to choose a card to summon
        print(f"{self.name}, choose a card to summon:")
        for i, card in enumerate(self.hand):
            print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
        card_index = int(input("Enter the number of the card: "))
        card = self.hand[card_index]

        # Check if the player has enough monsters to tribute
        monsters_on_field = [zone for zone in self.field.zones[self.name]["main_monster_zones"] if zone is not None]
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

        # Ask the player to choose a zone for the monster
        print("Choose a monster zone to place the card in (0: far-left, 1: left, 2: center, 3: right, 4: far-right):")
        zone_index = int(input())
        self.field.place_card(self.name, "main_monster_zones", card, zone_index)

        self.has_normal_summoned = True
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
