class Card:
    def __init__(self, name, level, card_type, atk, defense):
        self.name = name
        self.level = level
        self.card_type = card_type
        self.atk = atk
        self.defense = defense
        self.position = None  # 'attack', 'defense', or 'set'
        self.summon_requirement = 0 if level <= 4 else 1 if level <= 6 else 2

    def get_state(self):
        state = {
            "name": self.name,
            "level": self.level,
            "type": self.card_type,
            "position": self.position,
            "atk": self.atk,
            "def": self.defense,
        }
        return state
    
    def __str__(self):
        return f"{self.name}, ATK: {self.atk}, DEF: {self.defense}, Level: {self.level}"

    __repr__ = __str__
    
    def set_position(self, position):
        if position in ['attack', 'defense', 'set']:
            self.position = position
        else:
            print("Invalid position.")
