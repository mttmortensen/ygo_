from deck import Deck

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.deck = Deck()
        self.deck.shuffle()

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
                print(f"\nIt's {player.name}'s turn.")
                player.standby_phase()
                if player.deck.cards:  # Only execute the Draw Phase if the deck is not empty
                    player.draw_phase()
                    if len(player.hand) >= 7:  # Check if hand size exceeds 7
                        player.discard()  # Discard a card
                else:
                    print(f"{player.name}'s deck is empty. The game is over.")
                    return
                player.main_phase_1()
                player.battle_phase()
                player.main_phase_2()
                player.end_phase()