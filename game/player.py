from field import Field
from game_commands import get_user_input, check_field

class Player:
    def __init__(self, game, name, deck):
        self.name = name
        self.hand = []
        self.deck = deck
        self.game = game
        self.graveyard = []
        self.field = Field(self.name)
        self.has_normal_summoned = False
        self.can_summon = True
        self.life_points = 8000

    def get_state(self):
        state = [
            len(self.hand),
            len(self.field.zones[self.name]["main_monster_zones"]),
            len(self.deck.cards),
            len(self.graveyard),
            self.life_points,
            int(self.has_normal_summoned),
            int(self.can_summon),
        ]
        return state


    def draw(self):
        if self.deck.cards:  # Check if the deck is not empty
            card = self.deck.draw_card()
            self.hand.append(card)
            print(f"{self.name} drew {card}")
            self.show_hand()
            if len(self.hand) > 7:  # Check if hand size exceeds 7
                self.discard()  # Discard a card
        else:
            print(f"{self.name}'s deck is empty. The game is over.")
            return False
        return True
    
    def discard(self):
        print(f"{self.name}, your hand is full. Choose a card to discard:")
        for i, card in enumerate(self.hand):
            print(f"{i}: {card}")
        card_index = int(input("Enter the number of the card to discard: "))
        card = self.hand[card_index]
        self.hand.remove(card)  # Remove the card from the hand
        self.graveyard.append(card)  # Add the card to the graveyard
        print(f"{self.name} discarded {card} to the graveyard.")
        self.field.zones["graveyard"] = card  # Add the card to the player's graveyard zone on the field
        print(f"Player's Graveyard: {self.graveyard}")

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand}")
        print(f"{self.name} hand size is: {len(self.hand)}")

    def choose_card_to_summon(self, game):
        while True:
            print("Choose a monster to summon:")
            for i, card in enumerate(self.hand):
                print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
            card_index = get_user_input("Enter the number of the card: ", game)
            if card_index.isdigit() and int(card_index) in range(len(self.hand)):
                return self.hand[int(card_index)]
            else:
                print("Invalid get_user_input. Please enter a valid number.")
    
    def summon(self, game):
        if self.has_normal_summoned:
            print("You have already performed a Normal Summon this turn.")
            return
        while True:  # Adding a loop to keep asking until a valid summon is performed or the player chooses not to summon
            summon_type = get_user_input("Do you want to perform a normal summon or a tribute summon? (normal/tribute): ", game)
            summonable_monsters = self.filter_summonable_monsters(summon_type)

            if summon_type.lower() == 'tribute':
                card = self.perform_tribute_summon(summonable_monsters, game)
            else:
                card = self.perform_normal_summon(summonable_monsters, game)

            if card is not None:
                self.hand.remove(card)
                position = get_user_input("Enter the battle position for the monster ('attack' or 'set'): ", game)
                card.set_position(position)
                if position == 'set':
                    card.has_been_set = True
                zone_index = int(get_user_input("Choose a monster zone to place the card in (0: far-left, 1: left, 2: center, 3: right, 4: far-right):", game))
                self.field.place_card(self.name, "main_monster_zones", card, zone_index)
                card.summoning_sickness = True 
                self.has_normal_summoned = True
                self.can_summon = False
                break

    def filter_summonable_monsters(self, summon_type):
        if summon_type == "normal":
            return [card for card in self.hand if card.level <= 4]
        elif summon_type == "tribute":
            return [card for card in self.hand if card.level > 4 and len([zone for zone in self.field.zones[self.name]["main_monster_zones"] if zone is not None]) >= card.summon_requirement]
    
    def perform_tribute_summon(self, summonable_monsters, game): 
        # Check if the player has a monster in their hand that requires a tribute 
        tribute_monsters_in_hand = [card for card in self.hand if card.level > 4]
        if not tribute_monsters_in_hand: 
            print(f"{self.name}, you do not have any monsters in your hand that require a tribute.") 
            return None 

        # Check if the player has enough monsters on the field to tribute 
        monsters_on_field = [zone for zone in self.field.zones[self.name]["main_monster_zones"] if zone is not None and not zone.summoning_sickness] 
        if not monsters_on_field:  
            print(f"{self.name}, you do not have any monsters on your field to tribute.") 
            return None 

        # If the player has a valid monster to tribute and enough monsters on the field, ask them to choose a monster to tribute summon 
        print(f"{self.name}, choose a monster to tribute summon:") 
        for i, card in enumerate(tribute_monsters_in_hand):  # Use tribute_monsters_in_hand here 
            print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}") 
        card_index = int(get_user_input("Enter the number of the card: ", game)) 
        card = tribute_monsters_in_hand[card_index]  # Update the card variable 

        tribute_requirement = 2 if card.level >= 7 else 1
        if len(monsters_on_field) < tribute_requirement:  # Check if there are enough monsters on the field to tribute 
            print(f"{self.name}, you do not have enough monsters on your field to tribute.") 
            return None 

        # Ask the player to choose which monsters to tribute 
        tribute_monsters = [] 
        for _ in range(tribute_requirement): 
            print(f"{self.name}, choose a monster to tribute:") 
            for i, monster in enumerate(monsters_on_field): 
                print(f"{i}: {monster.name}") 
            monster_index = int(get_user_input("Enter the number of the monster: ", game)) 
            monster = monsters_on_field.pop(monster_index) 
            tribute_monsters.append(monster) 
            # Find the index of the monster in the monster zones
            monster_zone_index = self.field.zones[self.name]["main_monster_zones"].index(monster)
            # Set the zone to None
            self.field.zones[self.name]["main_monster_zones"][monster_zone_index] = None

        # Send the tribute monsters to the graveyard and print a message 
        for monster in tribute_monsters: 
            self.graveyard.append(monster) 
        print(f"Monster(s) {', '.join(monster.name for monster in tribute_monsters)} have been sent to the graveyard for tribute.") 

        return card

    def perform_normal_summon(self, summonable_monsters, game):
        # If the player wants to perform a normal summon, ask them to choose a card to summon
        print(f"{self.name}, choose a card to summon:")
        for i, card in enumerate(summonable_monsters):
            print(f"{i}: {card.name}, ATK: {card.atk}, DEF: {card.defense}, Level: {card.level}")
        card_index = int(get_user_input("Enter the number of the card: ", game))
        card = summonable_monsters[card_index]  # Update the card variable

        return card
    
    def change_positions(self, game):
        # Check if there are any monsters that can change their positions
        can_change_positions = any(zone is not None and zone.can_change_position for zone in self.field.zones[self.name]["main_monster_zones"])
        if not can_change_positions:
            print(f"{self.name} cannot change any monster's positions at this time.")
            return  # Skip to the next phase

        print(f"{self.name}, choose a monster to change it's position:")
        for i, zone in enumerate(self.field.zones[self.name]["main_monster_zones"]):
            if zone is not None and zone.can_change_position:  # Check if the monster can change position
                print(f"{i}: {zone.name}, Position: {zone.position}")
        card_index = int(get_user_input("Enter the number of the monster: ", game))
        monster = self.field.zones[self.name]["main_monster_zones"][card_index]
        if monster.position == 'attack':
            monster.position = 'defense'
        else:
            monster.position = 'attack'
        monster.has_changed_position = True
        monster.can_change_position = False
        print(f"{monster.name} is now in {monster.position} position.")

    def standby_phase(self):
        print(f"{self.name} is in the Standby Phase.")
        # Reset summoning status and position change status
        for zone in self.field.zones[self.name]["main_monster_zones"]:
            if zone is not None:
                zone.has_summoned = False
                zone.can_change_position = True

    def get_hand_size(self):
        return len(self.hand)

    def get_deck_size(self):
        return len(self.deck.cards)
