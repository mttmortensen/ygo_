
def get_user_input(prompt, game=None):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            confirm_exit = input("Are you sure you want to exit? (yes/no): ")
            if confirm_exit.lower() == 'yes':
                print("Thanks for playing!")
                exit()
        elif user_input.lower() == 'check-field' and game is not None:
            check_field(game)
        elif user_input.lower() == 'check-graveyard' and game is not None:
            check_graveyard(game)
        else:
            return user_input

def check_field(game):
    for player in game.players:
        print(f"{player.name}'s Life Points are: {player.life_points}")
        print(f"{player.name}'s hand size is: {len(player.hand)}")
        print(f"{player.name}'s deck size is: {len(player.deck.cards)}")
        print(f"{player.name}'s graveyard size is: {len(player.graveyard)}")
        print(f"{player.name}'s field:")
        for i, monster in enumerate(player.field.zones[player.name]["main_monster_zones"]):
            if monster is not None:
                print(f"  Monster Zone {i}: {monster.name}, ATK: {monster.atk}, DEF: {monster.defense}, Level: {monster.level} Position: {monster.position}")
            else:
                print(f"  Monster Zone {i}: Empty")

def check_graveyard(game):
    for player in game.players:
        print(f"{player.name}'s Graveyard:")
        if len(player.graveyard) == 0:
            print("[]")
        else:
            for card in player.graveyard:
                print(card)
