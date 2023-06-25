def get_user_input(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'exit':
        confirm_exit = input("Are you sure you want to exit? (yes/no): ")
        if confirm_exit.lower() == 'yes':
            print("Thanks for playing!")
            exit()
    return user_input

def print_game_state(game):
    for player in game.players:
        print(f"{player.name}'s deck size is: {len(player.deck.cards)}")
        print(f"{player.name}'s graveyard size is: {len(player.graveyard)}")
        print(f"{player.name}'s field:")
        for i, monster in enumerate(player.field.zones[player.name]["main_monster_zones"]):
            if monster is not None:
                print(f"  Monster Zone {i}: {monster.name}, ATK: {monster.atk}, DEF: {monster.defense}, Level: {monster.level} Position: {monster.position}")
            else:
                print(f"  Monster Zone {i}: Empty")
