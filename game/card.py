class Card:
    def __init__(self, name, level, card_type, atk, defense):
        self.name = name
        self.level = level
        self.card_type = card_type
        self.atk = atk
        self.defense = defense
        self.position = None  # 'attack', 'defense', or 'set'
        self.can_change_position = False
        self.has_changed_position = False
        self.summon_requirement = 0 if level <= 4 else 1 if level <= 6 else 2
        self.has_summoned = False
        self.has_attacked = False
        self.has_been_set = False


    def get_state(self):
        state = [
            self.level,
            self.atk,
            self.defense,
            1 if self.position == 'attack' else 0,  # Convert position to a binary value
        ]
        return state

    
    def __str__(self):
        return f"{self.name}, ATK: {self.atk}, DEF: {self.defense}, Level: {self.level}"

    __repr__ = __str__
    
    def set_position(self, position):
        if position in ['attack', 'defense', 'set']:
            self.position = position
        else:
            print("Invalid position.")
