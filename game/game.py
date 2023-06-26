from field import Field
from game_commands import get_user_input, check_field

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.turn = 0
        player1.field = Field(player1.name)
        player2.field = Field(player2.name)
        self.players[0].deck.shuffle()
        self.players[1].deck.shuffle()
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
            for i in range(2):  # Use range(2) instead of self.players
                player = self.players[i]
                opponent = self.players[1 - i]  # Get the opponent player
                player.has_normal_summoned = False  # Reset the normal summon status
                player.can_summon = True
                print(f"\nIt's {player.name}'s turn.")
                if player.deck.cards:  # Only execute the Draw Phase if the deck is not empty
                    self.current_phase = "Draw Phase"  # Update current_phase                  
                    player.draw_phase()
                    if len(player.hand) >= 7:  # Check if hand size exceeds 7
                        player.discard()  # Discard a card
                else: # Deck out win condition
                    print(f"{player.name}'s deck is empty. {opponent.name} wins the game!")
                    return
                if player.life_points <= 0: # Life Point win condition
                    print(f"{player.name}'s life points have reached 0. {opponent.name} wins the game! ")
                self.current_phase = "Standby Phase"  # Update current_phase
                player.standby_phase()
                self.current_phase = "Main Phase 1"  # Update current_phase
                player.main_phase_1()
                if player.can_summon:
                    summon_choice = get_user_input("Would you like to summon a monster? (yes/no): ", self)
                    if summon_choice.lower() == 'yes':
                        check_field(self)
                        player.summon(self)
                self.current_phase = "Battle Phase"  # Update current_phase
                player.battle_phase(opponent, self.turn, self)  # Pass the opponent player as an argument
                self.current_phase = "Main Phase 2"  # Update current_phase
                player.main_phase_2()
                if player.can_summon:
                    summon_choice = get_user_input("Would you like to summon a monster? (yes/no): ", self)
                    if summon_choice.lower() == 'yes':
                        player.summon(self)
                self.current_phase = "End Phase"  # Update current_phase
                player.end_phase()
                self.turn += 1  # Increment the turn count at the end of each player's turn
            for player in self.players: # Reseting monsters that have attacked  for this turn
                for zone in player.field.zones[player.name]["main_monster_zones"]:
                    if zone is not None:
                        zone.has_attacked = False

