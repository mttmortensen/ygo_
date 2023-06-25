class Card:
    def __init__(self, name, level, card_type):
        self.name = name
        self.level = level
        self.card_type = card_type
        self.position = None  # 'attack', 'defense', or 'set'
        self.summon_requirement = 0 if level <= 4 else 1 if level <= 6 else 2

    def set_position(self, position):
        if position in ['attack', 'defense', 'set']:
            self.position = position
        else:
            print("Invalid position.")
