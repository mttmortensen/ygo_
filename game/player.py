from deck import Deck
from field import Field
from game_utils import get_user_input
import random

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.hand = []
        self.deck = deck
        self.graveyard = []
        self.field = Field(self.name)
        self.has_normal_summoned = False
        self.can_summon = True

    def get_state(self):
        for card in self.hand:
            print(f"Card: {card}, Type: {type(card)}")
        state = {
            "name": self.name,
            "hand": [card.get_state() for card in self.hand],
            "field": self.field.get_state(),
            "deck_size": len(self.deck.cards),
            "has_normal_summoned": self.has_normal_summoned,
            "can_summon": self.can_summon,
        }
        return state

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
        print(f"Player's Graveyard: {self.graveyard}")

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")
        print(f"{self.name} hand size is: {len(self.hand)}")

    def choose_card_to_summon(self):
        while True:
            print("Choose a monster to summon:")
            for i, card in enumerate(self.hand):
                print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
            card_index = get_user_input("Enter the number of the card: ")
            if card_index.isdigit() and int(card_index) in range(len(self.hand)):
                return self.hand[int(card_index)]
            else:
                print("Invalid get_user_input. Please enter a valid number.")
    
    def summon(self):
        if self.has_normal_summoned:
            print("You have already performed a Normal Summon this turn.")
            return

        summon_type = get_user_input("Do you want to perform a normal summon or a tribute summon? (normal/tribute): ")
        summonable_monsters = self.filter_summonable_monsters(summon_type)

        if summon_type.lower() == 'tribute':
            card = self.perform_tribute_summon(summonable_monsters)
        else:
            card = self.perform_normal_summon(summonable_monsters)

        if card is not None:
            self.hand.remove(card)
            position = get_user_input("Enter the battle position for the monster ('attack' or 'set'): ")
            card.set_position(position)
            zone_index = int(get_user_input("Choose a monster zone to place the card in (0: far-left, 1: left, 2: center, 3: right, 4: far-right):"))
            self.field.place_card(self.name, "main_monster_zones", card, zone_index)
            self.has_normal_summoned = True
            self.can_summon = False

    def filter_summonable_monsters(self, summon_type):
        if summon_type == "normal":
            return [card for card in self.hand if card.level <= 4]
        elif summon_type == "tribute":
            return self.hand
    
    def perform_tribute_summon(self, summon_type):
        # If the player wants to perform a tribute summon, check if they have a valid monster to tribute
        if summon_type.lower() == 'tribute':
            # Check if the player has a monster in their hand that requires a tribute
            if all(card.level <= 4 for card in self.hand):
                print(f"{self.name}, you do not have any monsters in your hand to tribute.")
                return self.summon()  # Ask the player again if they want to perform a normal summon or a tribute summon

            # Check if the player has enough monsters on the field to tribute
            monsters_on_field = [zone for zone in self.field.zones[self.name]["main_monster_zones"] if zone is not None]
            if len(monsters_on_field) < 1:  # Change this to the actual tribute requirement of the monster
                print(f"{self.name}, you do not have any monsters on your field to tribute.")
                return self.summon()  # Ask the player again if they want to perform a normal summon or a tribute summon

            # If the player has a valid monster to tribute and enough monsters on the field, ask them to choose a monster to tribute summon
            print(f"{self.name}, choose a monster to tribute summon:")
            for i, card in enumerate(summonable_monsters):  # Use summonable_monsters here
                print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
            card_index = int(get_user_input("Enter the number of the card: "))
            card = summonable_monsters[card_index]  # Update the card variable

            # Ask the player to choose which monsters to tribute
            tribute_monsters = []
            for _ in range(card.summon_requirement):
                print(f"{self.name}, choose a monster to tribute:")
                for i, monster in enumerate(monsters_on_field):
                    print(f"{i}: {monster.name}")
                monster_index = int(get_user_input("Enter the number of the monster: "))
                monster = monsters_on_field.pop(monster_index)
                tribute_monsters.append(monster)
                self.field.zones[self.name]["main_monster_zones"].remove(monster)

            # Send the tribute monsters to the graveyard and print a message
            for monster in tribute_monsters:
                self.graveyard.append(monster)
            print(f"Monster(s) {', '.join(monster.name for monster in tribute_monsters)} have been sent to the graveyard for tribute.")

    def perform_normal_summon(self, summonable_monsters):
        # If the player wants to perform a normal summon, ask them to choose a card to summon
        print(f"{self.name}, choose a card to summon:")
        for i, card in enumerate(summonable_monsters):
            print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
        card_index = int(get_user_input("Enter the number of the card: "))
        card = summonable_monsters[card_index]  # Update the card variable

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
