def battle_phase(self, opponent, current_turn, game):
        print(f"{self.name} is in the Battle Phase.")
        print("Start Step begins.")
        print("Battle Step begins.")
        action = get_user_input("Do you want to attack with a monster or end your Battle Phase? (attack/end): ", game)
        if action.lower() == "attack":
            # Battle Step
            # Check if there are any monsters in attack position that can still attack
            
                # Check if there are any monsters that can still attack
                
                               
                        # Direct attack
                        
                        # Check if opponent's life points have reached 0 or less
                        
                        
                    else:
                        if len(opponent.field.zones[opponent.name]["main_monster_zones"]) > 0:

                            # Damage Step
                           
                            if attacking_card.atk > defending_card.atk and defending_card.position == "attack":
                                print(f"{defending_card.name} is destroyed by battle.")
                                opponent.graveyard.append(defending_card)
                                opponent.field.zones[opponent.name]["main_monster_zones"][card_index] = None
                                opponent.life_points -= attacking_card.atk - defending_card.atk  # Subtracting life points
                                print(f"{opponent.name} loses {attacking_card.atk - defending_card.atk} life points.")
                            # Check if opponent's life points have reached 0 or less
                            if opponent.life_points <= 0:
                                print(f"{opponent.name}'s life points have reached 0.")
                                print(f"{self.name} is the winner!")
                                game.game_over = True
                                game.end_game()  
                                return
                            elif self.life_points <= 0:
                                print(f"{self.name}'s life points have reached 0.")
                                print(f"{opponent.name} is the winner!")
                                game.game_over = True
                                game.end_game()  
                                return
                            # Battle Damage Calculation
                            elif attacking_card.atk == defending_card.atk and defending_card.position == "attack":
                                print(f"Both {attacking_card.name} and {defending_card.name} went to the Graveyard")
                                opponent.graveyard.append(defending_card)
                                opponent.field.zones[opponent.name]["main_monster_zones"][card_index] = None
                                self.graveyard.append(attacking_card)
                                self.field.zones[self.name]["main_monster_zones"][card_index] = None
                            elif attacking_card.atk > defending_card.defense and defending_card.position == "defense":
                                print(f"{defending_card.name} is destroyed by battle.")
                                opponent.graveyard.append(defending_card)
                                opponent.field.zones[opponent.name]["main_monster_zones"][card_index] = None
                            elif attacking_card.atk < defending_card.atk and defending_card.position == "attack":
                                print(f"{attacking_card.name} is destoryed by battle and sent to the {self.name}'s Graveyard")
                                self.graveyard.append(attacking_card)
                                self.field.zones[self.name]["main_monster_zones"][card_index] = None
                                self.life_points -= defending_card.atk - attacking_card.atk  # Subtracting life points
                                # Check if opponent's life points have reached 0 or less
                                if opponent.life_points <= 0:
                                    print(f"{opponent.name}'s life points have reached 0.")
                                    print(f"{self.name} is the winner!")
                                    game.game_over = True
                                    game.end_game()  
                                    return
                                elif self.life_points <= 0:
                                    print(f"{self.name}'s life points have reached 0.")
                                    print(f"{opponent.name} is the winner!")
                                    game.game_over = True
                                    game.end_game()  
                                    return
                                print(f"{self.name} loses {defending_card.atk - attacking_card.atk} life points.")
                            elif attacking_card.atk < defending_card.defense and defending_card.position == "defense":
                                self.life_points -= defending_card.defense - attacking_card.atk  # Subtracting life points
                                # Check if opponent's life points have reached 0 or less
                                if opponent.life_points <= 0:
                                    print(f"{opponent.name}'s life points have reached 0.")
                                    print(f"{self.name} is the winner!")
                                    game.game_over = True
                                    game.end_game()  
                                    return
                                elif self.life_points <= 0:
                                    print(f"{self.name}'s life points have reached 0.")
                                    print(f"{opponent.name} is the winner!")
                                    game.game_over = True
                                    game.end_game()
                                    return
                                print(f"{self.name} loses {defending_card.defense - attacking_card.atk} life points.")

                            print(f"{self.name}'s life points: {self.life_points}")
                            print(f"{opponent.name}'s life points: {opponent.life_points}")
                            print("Damage Step ends.")
                else:
                    print(f"{attacking_card.name} cannot attack this turn because it has summoning sickness.")
            

                continue_battle = get_user_input("Do you want to continue the Battle Phase? (yes/no): ", game)
                if continue_battle.lower() == "yes":
                    # Check if there are any monsters that can still attack
                    can_attack = any(zone is not None and not zone.has_attacked for zone in self.field.zones[self.name]["main_monster_zones"])
                    if not can_attack:
                        print(f"{self.name}, you have no more monsters to attack with.")
                        return  # Skip to the next phase  
                    # End Damage Step
                else:
                    print("End Damgage Step.")
                    print(f"{self.name}'s Battle Phase ends.")
                    break
        elif action.lower() == "end":
            # End Step
            print("End Damage Step.")
            print(f"{self.name}'s Battle Phase ends.")



def start_battle_step(self, opponent, current_turn, game):
    can_attack = any(zone is not None and not zone.has_attacked and zone.position == "attack" and not zone.has_summoned for zone in self.field.zones[self.name]["main_monster_zones"])
    if not can_attack:
        print(f"{self.name}, you have no monsters in attack position to attack with.")
        return  # Skip to the next phase
    if current_turn == 0:  # Check if it's the first turn of the duel
        print("You cannot attack on the first turn of the duel.")
        print("End Step begins.")
        return
    while not game.game_over:  # Add a loop to allow multiple battles
        self.perform_battle(opponent, game)

def perform_battle(self, opponent, game):
    can_attack = any(zone is not None and not zone.has_attacked and zone.position == "attack" and not zone.has_summoned for zone in self.field.zones[self.name]["main_monster_zones"])
    if not can_attack:
        print(f"{self.name}, you have no more monsters to attack with.")
        return  # Skip to the next phase
    attacking_card = self.select_monster_to_attack_with(game)
    # Check if the monster has summoning sickness
    if not attacking_card.has_attacked and not attacking_card.summoning_sickness:
        # Check if there are any monsters on the opponent's field
        opponent_has_monsters = any(zone is not None for zone in opponent.field.zones[opponent.name]["main_monster_zones"])
        if not opponent_has_monsters:
            self.direct_attack(opponent, attacking_card, game)
        else: 
            self.attack_monser(opponent, attacking_card, game)

def select_monster_to_ack_with(self, game):
    print(f"{self.name}, choose a monster to attack with:")
    for i, zone in enumerate(self.field.zones[self.name]["main_monster_zones"]):
        if zone is not None and not zone.has_attacked and zone.position == "attack" and not zone.has_summoned:
            print(f"{i}: {zone.name}, ATK: {zone.atk}, DEF: {zone.defense}, Level: {zone.level}, Position: {zone.position}")
    card_index = int(get_user_input("Enter the number of the card: ", game))
    return self.field.zonez[self.name]["main_monster_zones"][card_index]

def direct_attack(self, opponent, attacking_card, game):
    print(f"{attacking_card.name} attacks {opponent.name}'s life points directly.")
    opponent.life_points -= attacking_card.atk
    self.check_game_over(opponent, game)
    print(f"{opponent.name} loses {attacking_card.atk} life points.")
    attacking_card.has_attacked = True

def attack_monster(self, opponent, attacking_card, game):
    print(f"{self.name}, choose a monster to attack:")
    for i, zone in enumerate(opponent.field.zones[opponent.name]["main_monster_zones"]):
        if zone is not None:
            print(f"{i}: {zone.name}, ATK: {zone.atk}, DEF: {zone.defense}, Level: {zone.level}, Position: {zone.position}")  # Corrected here
    card_index = int(get_user_input("Enter the number of the card: ", game))
    defending_card = opponent.field.zones[opponent.name]["main_monster_zones"][card_index]

    print(f"{attacking_card.name} attacks {defending_card.name}.")
    attacking_card.has_attacked = True
    self.damage_step(opponent, attacking_card, defending_card, game)

def damage_step(self, opponent, attacking_card, defending_card, game):
    print("Damage Step begins.")
    if defending_card.position == "set":
        print(f"{defending_card.name} is flipped face-up.")
        defending_card.set_position("defense")  # Assume that a flipped monster is in defense position
        defending_card.has_been_set = False
    self.battle_damage_calculation(opponent, attacking_card, defending_card, game)

def battle_damage_calculation(opponent, attacking_card, defending_card, game):

def check_game_over(self, opponent, game):
    if opponent.life_points <= 0:
        print(f"{opponent.name}'s life points have reached 0.")
        print(f"{self.name} is the winner!")
        game.game_over = True
        game.end_game()  # Assuming you have a method to end the game
        return True
    elif self.life_points <= 0:
        print(f"{self.name}'s life points have reached 0.")
        print(f"{opponent.name} is the winner!")
        game.game_over = True
        game.end_game()  # Assuming you have a method to end the game
        return True
    return False
     