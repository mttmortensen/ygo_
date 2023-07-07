from game_commands import get_user_input

class BattlePhase:
    def __init__(self, player, opponent, game):
        self.player = player
        self.opponent = opponent
        self.game = game

    def battle_phase(self):
        print(f"{self.player.name} is in the Battle Phase.")
        print("Start Step begins.")
        print("Battle Step begins.")
        action = get_user_input("Do you want to attack with a monster or end your Battle Phase? (attack/end): ", self.game)
        if action.lower() == "attack":
            # Battle Step
            self.start_battle_step()
        elif action.lower() == "end":
            # End Step
            self.end_battle_phase()

    def start_battle_step(self):
        can_attack = any(zone is not None and not zone.has_attacked and zone.position == "attack" and not zone.has_summoned for zone in self.player.field.zones[self.player.name]["main_monster_zones"])
        if not can_attack:
            print(f"{self.player.name}, you have no monsters in attack position to attack with.")
            return  # Skip to the next phase
        if self.game.turn == 0:  # Check if it's the first turn of the duel
            print("You cannot attack on the first turn of the duel.")
            print("End Step begins.")
            return
        while not self.game.game_over:  # Add a loop to allow multiple battles
            self.perform_battle()

    def perform_battle(self):
        can_attack = any(zone is not None and not zone.has_attacked and zone.position == "attack" and not zone.has_summoned for zone in self.player.field.zones[self.player.name]["main_monster_zones"])
        if not can_attack:
            print(f"{self.player.name}, you have no more monsters to attack with.")
            return  # Skip to the next phase
        attacking_card = self.select_monster_to_ack_with()
        # Check if the monster has summoning sickness
        if not attacking_card.has_attacked and not attacking_card.summoning_sickness:
            # Check if there are any monsters on the opponent's field
            opponent_has_monsters = any(zone is not None for zone in self.opponent.field.zones[self.opponent.name]["main_monster_zones"])
            if not opponent_has_monsters:
                self.direct_attack(attacking_card)
            else: 
                self.attack_monser(attacking_card)

    def select_monster_to_ack_with(self):
        print(f"{self.player.name}, choose a monster to attack with:")
        for i, zone in enumerate(self.player.field.zones[self.player.name]["main_monster_zones"]):
            if zone is not None and not zone.has_attacked and zone.position == "attack" and not zone.has_summoned:
                print(f"{i}: {zone.name}, ATK: {zone.atk}, DEF: {zone.defense}, Level: {zone.level}, Position: {zone.position}")
        card_index = int(get_user_input("Enter the number of the card: ", self.game))
        return self.player.field.zones[self.player.name]["main_monster_zones"][card_index]

    def direct_attack(self, attacking_card):
        print(f"{attacking_card.name} attacks {self.opponent.name}'s life points directly.")
        self.opponent.life_points -= attacking_card.atk
        self.game.check_game_over(self.opponent, self.game)
        print(f"{self.opponent.name} loses {attacking_card.atk} life points.")
        attacking_card.has_attacked = True

    def attack_monster(self, attacking_card):
        print(f"{self.player.name}, choose a monster to attack:")
        for i, zone in enumerate(self.opponent.field.zones[self.opponent.name]["main_monster_zones"]):
            if zone is not None:
                print(f"{i}: {zone.name}, ATK: {zone.atk}, DEF: {zone.defense}, Level: {zone.level}, Position: {zone.position}")  # Corrected here
        card_index = int(get_user_input("Enter the number of the card: ", self.game))
        defending_card = self.opponent.field.zones[self.opponent.name]["main_monster_zones"][card_index]
        print(f"{attacking_card.name} attacks {defending_card.name}.")
        attacking_card.has_attacked = True
        self.damage_step(attacking_card, defending_card, card_index)

    def damage_step(self, attacking_card, defending_card, card_index):
        print("Damage Step begins.")
        if defending_card.position == "set":
            print(f"{defending_card.name} is flipped face-up.")
            defending_card.set_position("defense")  # Assume that a flipped monster is in defense position
            defending_card.has_been_set = False
        self.battle_damage_calculation(attacking_card, defending_card, card_index)

    def battle_damage_calculation(self, attacking_card, defending_card, card_index):
        # ATTACKING MONSTER ATK > DEFENDING MONSTER ATK
        if attacking_card.atk > defending_card.atk and defending_card.position == "attack":
            print(f"{defending_card.name} is destroyed by battle.")
            self.opponent.graveyard.append(defending_card)
            self.opponent.field.zones[self.opponent.name]["main_monster_zones"][card_index] = None
            self.opponent.life_points -= attacking_card.atk - defending_card.atk  # Subtracting life points
            print(f"{self.opponent.name} loses {attacking_card.atk - defending_card.atk} life points.")
            self.game.check_game_over(self.opponent, self.game)
        # ATTACKING MONSTER ATK = DEFENDING MONSTER ATK
        elif attacking_card.atk == defending_card.atk and defending_card.position == "attack":
            print(f"Both {attacking_card.name} and {defending_card.name} went to the Graveyard")
            self.opponent.graveyard.append(defending_card)
            self.opponent.field.zones[self.opponent.name]["main_monster_zones"][card_index] = None
            attacking_card.graveyard.append(attacking_card)
            attacking_card.field.zones[attacking_card.name]["main_monster_zones"][card_index] = None
            self.game.check_game_over(self.opponent, self.game)
        # ATTACKING MONSTER ATK > DEFENDING MOSNTER DEF. NO LP LOST
        elif attacking_card.atk > defending_card.defense and defending_card.position == "defense":
            print(f"{defending_card.name} is destroyed by battle.")
            self.opponent.graveyard.append(defending_card)
            self.opponent.field.zones[self.opponent.name]["main_monster_zones"][card_index] = None
            self.game.check_game_over(self.opponent, self.game)
        # ATTACKING MONSTER ATK < DEFENDING MONSTER ATK
        elif attacking_card.atk < defending_card.atk and defending_card.position == "attack":
            print(f"{attacking_card.name} is destoryed by battle and sent to the {attacking_card.name}'s Graveyard")
            attacking_card.graveyard.append(attacking_card)
            attacking_card.field.zones[attacking_card.name]["main_monster_zones"][card_index] = None
            attacking_card.life_points -= defending_card.atk - attacking_card.atk  # Subtracting life points
            self.game.check_game_over(self.opponent, self.game)
        # ATTACKING MONSTER ATK < DEFENDING MOSNTER DEF
        elif attacking_card.atk < defending_card.defense and defending_card.position == "defense":
            attacking_card.life_points -= defending_card.defense - attacking_card.atk  # Subtracting life points
            print(f"{self.name} loses {defending_card.defense - attacking_card.atk} life points.")
            self.game.check_game_over(self.opponent, self.game)
        # ATTACKING MONSTER ATK = DEFENDING MONSTER DEF. NO LP LOST
        elif attacking_card.atk == defending_card.defense and defending_card.position == "defense":
            print(f"No monsters are destroyed and no life points are lost.")

    def end_battle_phase(self):
        continue_battle = get_user_input("Do you want to continue the Battle Phase? (yes/no): ", self.game)
        if continue_battle.lower() == "yes":
            # Check if there are any monsters that can still attack
            can_attack = any(zone is not None and not zone.has_attacked for zone in self.player.field.zones[self.player.name]["main_monster_zones"])
            if not can_attack:
                print(f"{self.name}, you have no more monsters to attack with.")
                return  # Skip to the next phase  
            # End Damage Step
        else:
            print("End Damgage Step.")
            print(f"{self.player.name}'s Battle Phase ends.")