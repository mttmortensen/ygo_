class Field:
    def __init__(self, player_name):
        self.player_name = player_name
        self.zones = {
            self.player_name: {
                "main_monster_zones": [None, None, None, None, None],
                "spell_and_trap_zones": [None, None, None, None, None],
                "field_zone": None,
                "graveyard": [],
                "extra_deck": [],
                "banished": [],
            },
            # EM Zones can be access by both players
            "extra_monster_zones": [None, None],
        }

        def get_state(self):
            state = {
                "zones": self.zones,
            }
            return state

    def place_card(self, player, zone_type, card, position=None):
        # Check Main Monster and Spell/Traps Zones first
        if zone_type in ["main_monster_zones", "spell_trap_zones"]:
            if position is not None and self.zones[player][zone_type][position] is None:
                self.zones[player][zone_type][position] = card
            else:
                print("Invalid position or position already occupied.")
        # Then the rest of the field excpet EM Zones
        elif zone_type in ["field_zone", "deck_zone", "extra_deck_zone", "graveyard"]:
            if self.zones[player][zone_type] is None:
                self.zones[player][zone_type] = card
            else:
                print("Zone already occupied.")
        # Checking the EM Zones
        elif zone_type == "extra_monster_zones":
            if position is not None and self.zones[zone_type][position] is None:
                self.zones[zone_type][position] = card
            else:
                print("Invalid position or position already occupied.")
        else:
            print("Invalid zone type.")

    # Same Concept as place_card but now removing the card
    def remove_card(self, player, zone_type, position=None):
        if zone_type in ["main_monster_zones", "spell_trap_zones"]:
            if position is not None and self.zones[player][zone_type][position] is not None:
                self.zones[player][zone_type][position] = None
            else:
                print("Invalid position or no card in position.")
        elif zone_type in ["field_zone", "deck_zone", "extra_deck_zone", "graveyard"]:
            if self.zones[player][zone_type] is not None:
                self.zones[player][zone_type] = None
            else:
                print("No card in zone.")
        elif zone_type == "extra_monster_zones":
            if position is not None and self.zones[zone_type][position] is not None:
                self.zones[zone_type][position] = None
            else:
                print("Invalid position or no card in position.")
        else:
            print("Invalid zone type.")
