from deck import Deck
from field import Field

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        player1.field = Field(player1.name)
        player2.field = Field(player2.name)
        self.deck = Deck()
        self.deck.shuffle()

    def get_state(self):
        state = {
            "phase": self.current_phase,
            "players": [player.get_state() for player in self.players],
            "field": self.field.get_state(),
        }
        return state

    def start(self):
        # Each player draws 5 cards
        print("Begin the duel...")
        for player in self.players:
            for _ in range(5):
                player.draw()

        # Game continues until a player's deck is empty
        while True:
            for player in self.players:
                player.has_normal_summoned = False  # Reset the normal summon status
                player.can_summon = True
                print(f"\nIt's {player.name}'s turn.")
                player.standby_phase()
                if player.deck.cards:  # Only execute the Draw Phase if the deck is not empty
                    player.draw_phase()
                    if len(player.hand) >= 7:  # Check if hand size exceeds 7
                        player.discard()  # Discard a card
                else:
                    print(f"{player.name}'s deck is empty. The game is over.")
                    return
                print(f"{player.name} is in Main Phase 1.")
                if player.can_summon:
                    summon_choice = input("Would you like to summon a monster? (yes/no): ")
                    if summon_choice.lower() == 'yes':
                        player.summon()
                print(f"{player.name} is in the Battle Phase.")
                print(f"{player.name} is in Main Phase 2.")
                if player.can_summon:
                    summon_choice = input("Would you like to summon a monster? (yes/no): ")
                    if summon_choice.lower() == 'yes':
                        player.summon()
                player.end_phase()