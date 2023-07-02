class YGOEnvironment:
    def __init__(self, player, game):
        self.state = None
        self.player = player
        self.game = game
        self.reset()
    
    def reset(self):
        # Initialize or reset the game state
        self.state = {
            'player_life_points': 8000,
            'opponent_life_points': 8000,
            # Lists out the players hands, graveyards
            'player_hand': [],
            'player_graveyard': [],
            'opponent_hand': [],
            'opponent_graveyard': []
        }
        return self.state
    
    def step(self, action):
        # Update the game state based on the action taken by the AI
        if action == 'normal':
            pass
        elif action == 'tribute':
            # Code to handle tribute summon
            pass
        elif action == 'attack':
            # Code to handle attack
            pass
        elif action == 'set':
            # Code to handle setting a monster
            pass
        elif action == 'end':
            # Code to handle ending the turn
            pass
        elif action == 'yes':
            # Code to handle saying yes to prompts
            pass
        elif action == 'no':
            # Code to handle saying no to prompts
            pass
        elif action == 'check-field':
            # Code to handle checking the field
            pass
        elif action == 'check-graveyard':
            # Code to handle checking the graveyard
            pass
        elif isinstance(action, int) and 0 <= action <= 6:
            # Code to handle selecting a card or a zone
            pass
        else: 
            raise ValueError(f"Invalid action: {action}")
        
    def calculdate_reward(self, player, opponent, game):
        reward = 0

        # Will have to add these properties to Player, in battle phase, damage step?

        # Rewarding the player for taking away LP
        reward += (opponent.starting_life_points - opponent.current_life_points)

        # Penalize the player for losing its own LP
        reward -= (player.starting_life_points - player.current_life_points)

        