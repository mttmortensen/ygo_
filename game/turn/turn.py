from game_commands import get_user_input, check_field
from battle_phase import battle_phase

class Turn:
    def __init__(self, player, opponent, game):
        self.player = player
        self.opponent = opponent
        self.game = game
        self.current_phase = None

    def play_turn(self):
        print(f"\nIt's {self.player.name}'s turn.")
        if self.player.deck.cards:  # Only execute the Draw Phase if the deck is not empty
            self.current_phase = "Draw Phase"  # Update current_phase                  
            self.player.draw_phase()
            if len(self.player.hand) >= 7:  # Check if hand size exceeds 7
                self.player.discard()  # Discard a card
        else: # Deck out win condition
            print(f"{self.player.name}'s deck is empty. {self.opponent.name} wins the game!")
            self.game.game_over = True
            self.game.end_game()
            return
        if self.player.life_points <= 0: # Life Point win condition
            print(f"{self.player.name}'s life points have reached 0. {self.opponent.name} wins the game! ")
            self.game.end_game()
            self.game.game_over = True
            return
        elif self.opponent.life_points <= 0:
            print(f"{self.opponent.name}'s life points have reached 0. {self.player.name} wins the game! ")
            self.game.end_game()
            self.game.game_over = True  
            return
        else:
            self.current_phase = "Standby Phase"  # Update current_phase
            self.standby_phase()
            if self.game.game_over:
                return
            self.current_phase = "Main Phase 1"  # Update current_phase
            self.main_phase_1()
            if self.game.game_over:
                return
            self.current_phase = "Battle Phase"  # Update current_phase
            battle_phase(self, self.opponent, self.game.turn, self.game)  # Pass the opponent player as an argument
            if self.game.game_over:
                return
            self.current_phase = "Main Phase 2"  # Update current_phase
            self.main_phase_2()
            if self.game.game_over:
                return
            self.current_phase = "End Phase"  # Update current_phase
            self.end_phase()

    def standby_phase(self):
        print(f"{self.name} is in the Standby Phase.")
        # Reset summoning status and position change status
        for zone in self.player.field.zones[self.player.name]["main_monster_zones"]:
            if zone is not None:
                zone.has_summoned = False
                zone.can_change_position = True

    def draw_phase(self):
        print(f"{self.player.name} is in the Draw Phase.")
        return self.player.draw()

    def main_phase_1(self):
        print(f"{self.player.name} is in Main Phase 1.")
        self.player.can_summon = True
        if self.player.can_summon:
            summon_choice = get_user_input("Would you like to summon a monster? (yes/no): ", self.game)
            if summon_choice.lower() == 'yes':
                check_field(self.game)
                self.player.summon(self)
        change_position_choice = get_user_input("Would you like to change a monster's position? (yes/no): ", self.game)
        if change_position_choice.lower() == 'yes':
            self.player.change_positions(self)

    def main_phase_2(self):
        print(f"{self.player.name} is in Main Phase 2.")
        self.player.can_summon = True
        if self.player.can_summon:
            summon_choice = get_user_input("Would you like to summon a monster? (yes/no): ", self.game)
            if summon_choice.lower() == 'yes':
                self.player.summon(self)
                check_field(self.game)
        change_position_choice = get_user_input("Would you like to change a monster's position? (yes/no): ", self.game)
        if change_position_choice.lower() == 'yes':
            self.player.change_positions(self)

    def end_phase(self):
        print(f"{self.player.name} is in the End Phase.")
        for zone in self.player.field.zones[self.player.name]["main_monster_zones"]:
            if zone is not None:
                zone.can_change_position = True
                zone.summoning_sickness = False