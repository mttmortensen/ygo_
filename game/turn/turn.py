class Turn:
    def __init__(self, player, opponent, game):
        self.player = player
        self.opponent = opponent
        self.game = game

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
            self.player.standby_phase()
            if self.game.game_over:
                return
            self.current_phase = "Main Phase 1"  # Update current_phase
            self.player.main_phase_1()
            if self.game.game_over:
                return
            self.current_phase = "Battle Phase"  # Update current_phase
            self.player.battle_phase(self.opponent, self.turn, self)  # Pass the opponent player as an argument
            if self.game.game_over:
                return
            self.current_phase = "Main Phase 2"  # Update current_phase
            self.player.main_phase_2()
            if self.game.game_over:
                return
            self.current_phase = "End Phase"  # Update current_phase
            self.player.end_phase()