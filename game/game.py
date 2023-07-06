from turn import Turn

class Game:
    def __init__(self):
        self.players = []
        self.turn = 0
        self.game_over = False

    def get_state(self):
        state = [
            player.get_state() for player in self.players
        ]
        # Flatten the list of lists into a single list
        state = [item for sublist in state for item in sublist]
        return state


    def start_game(self):
        # Each player draws 5 cards
        print("Begin the duel...")
        for player in self.players:
            for _ in range(5):
                player.draw()
        # Game continues until a player's deck is empty
        while not self.game_over:
            for i in range(2):  # Use range(2) instead of self.players
                player = self.players[i]
                opponent = self.players[1 - i]  # Get the opponent player
                # Resetting status'
                player.has_normal_summoned = False  
                player.can_summon = True
                for zone in player.field.zones[player.name]["main_monster_zones"]:
                    if zone is not None:
                        zone.can_change_position = True
                        zone.has_changed_position = False
                turn = Turn(player, opponent, self)
                turn.play_turn()
                if self.check_game_over():  # Check if the game is over after each turn
                    break
                self.turn += 1  # Increment the turn count at the end of each player's turn
            if self.game_over:
                break
            for player in self.players: # Reseting monsters that have attacked  for this turn
                for zone in player.field.zones[player.name]["main_monster_zones"]:
                    if zone is not None:
                        zone.has_attacked = False

    def check_game_over(self, player, opponent):
        if opponent.life_points <= 0:
            print(f"{opponent.name}'s life points have reached 0.")
            print(f"{player.name} is the winner!")
            self.game_over = True
            self.end_game()
            return True
        elif player.life_points <= 0:
            print(f"{player.name}'s life points have reached 0.")
            print(f"{opponent.name} is the winner!")
            self.game_over = True
            self.end_game()
            return True
        elif not player.deck.cards:  # Deck out win condition
            print(f"{player.name}'s deck is empty. {opponent.name} wins the game!")
            self.game_over = True
            self.end_game()
            return True
        return False

    
    def end_game(self):
        # Reset the game state
        self.players = []
        self.current_phase = None
        self.turn = 0

        # Print a message to indicate that the game has ended
        print("The game has ended. Thanks for playing!")


