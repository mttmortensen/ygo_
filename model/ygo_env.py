class YGOEnvironment:
    def __init__(self):
        self.state = None
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