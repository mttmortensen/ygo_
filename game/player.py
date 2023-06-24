from deck import Deck

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = Deck()

    def draw(self):
        if self.deck.cards:  # Check if the deck is not empty
            card = self.deck.draw_card()
            self.hand.append(card)
            print(f"{self.name} drew {card}")
            self.show_hand()
        else:
            return False
        return True

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")
        print(f"{self.name} hand size is: {len(self.hand)}")
        print(f"{self.name} deck size is: {len(self.deck.cards)}")
    
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

    def get_hand_size(self):
        return len(self.hand)

    def get_deck_size(self):
        return len(self.deck.cards)
