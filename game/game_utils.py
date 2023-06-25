def get_user_input(prompt):
    user_input = input(prompt)
    if user_input.lower() == 'exit':
        confirm_exit = input("Are you sure you want to exit? (yes/no): ")
        if confirm_exit.lower() == 'yes':
            print("Thanks for playing!")
            exit()
    return user_input
