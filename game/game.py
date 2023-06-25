from deck import Deck
from field import Field

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        player1.field = Field(player1.name)
        player2.field = Field(player2.name)
        self.deck = Deck()
        self.deck.shuffle()
        self.current_phase = None

    def get_state(self):
        return {
            "players": [player.get_state() for player in self.players],
            "current_phase": self.current_phase,
        }

    def start_game(self):
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
                self.current_phase = "Standby Phase"  # Update current_phase
                player.standby_phase()
                if player.deck.cards:  # Only execute the Draw Phase if the deck is not empty
                    self.current_phase = "Draw Phase"  # Update current_phase                  
                    player.draw_phase()
                    if len(player.hand) >= 7:  # Check if hand size exceeds 7
                        player.discard()  # Discard a card
                else:
                    print(f"{player.name}'s deck is empty. The game is over.")
                    return
                print(f"{player.name} is in Main Phase 1.")
                self.current_phase = "Main Phase 1"  # Update current_phase
                player.main_phase_1()
                if player.can_summon:
                    summon_choice = input("Would you like to summon a monster? (yes/no): ")
                    if summon_choice.lower() == 'yes':
                        player.summon()
                print(f"{player.name} is in the Battle Phase.")
                self.current_phase = "Battle Phase"  # Update current_phase
                player.battle_phase()
                print(f"{player.name} is in Main Phase 2.")
                self.current_phase = "Main Phase 2"  # Update current_phase
                player.main_phase_2()
                if player.can_summon:
                    summon_choice = input("Would you like to summon a monster? (yes/no): ")
                    if summon_choice.lower() == 'yes':
                        player.summon()
                self.current_phase = "End Phase"  # Update current_phase
                player.end_phase()
