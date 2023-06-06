# Import necessary libraries
import numpy as np

# Define the TicTacToe class
class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3,3))
        self.x = -1  # player 'x'
        self.o = 1   # player 'o'
        self.none = 0  # no player
        self.win_reward = 1.0
        self.defeat_reward = -1.0
        self.draw_reward = 0.5
        self.players = [self.x, self.o]

    def is_end(self):
        # Vertical win
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != self.none:
                return self.board[0][i]
        # Horizontal win
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != self.none:
                return self.board[i][0]
        # Main diagonal win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != self.none:
            return self.board[0][0]
        # Second diagonal win
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != self.none:
            return self.board[0][2]
        # Is whole board full?
        for i in range(3):
            for j in range(3):
                # There's an empty field, we continue the game
                if self.board[i][j] == self.none:
                    return self.none
        # It's a tie!
        return 'TIE'

    def valid_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == self.none]

    def make_move(self, player, i, j):
        if self.board[i][j] == self.none:
            self.board[i][j] = player
            result = self.is_end()
            if result == player:
                return self.win_reward
            elif result == 'TIE':
                return self.draw_reward
            else:  # Game is not over yet
                return 0.0
        else:
            return self.defeat_reward  # Invalid move

# Define the QLearningAgent class
class QLearningAgent:
    def __init__(self, alpha=0.5, discount_factor=0.95, exploration_rate=1.0, exploration_decay_rate=0.995):
       self.alpha = alpha  # learning rate
       self.discount_factor = discount_factor  # discount factor for future rewards
       self.exploration_rate = exploration_rate  # exploration rate (epsilon)
       self.exploration_decay_rate = exploration_decay_rate  # exploration decay rate (epsilon decay)
       self.q_table = dict()  # Q table

    def get_q_value(self, state, action):
        return self.q_table.get((state.tobytes(), action), 0.0)

    def update_q_value(self, state, action, reward, next_max_q_value):
        old_q_value = self.get_q_value(state, action)
        new_q_value = (1.0 - self.alpha) * old_q_value + self.alpha * (reward + self.discount_factor * next_max_q_value)
        self.q_table[(state.tobytes(), action)] = new_q_value

    def choose_action(self, state, valid_actions):
        if np.random.uniform(0, 1) < self.exploration_rate:  # explore
            return valid_actions[np.random.randint(0, len(valid_actions))]
        else:  # exploit
            q_values = [self.get_q_value(state, action) for action in valid_actions]
            return valid_actions[np.argmax(q_values)]
    
    def decay_exploration_rate(self):
        self.exploration_rate *= self.exploration_decay_rate

# Define helper functions for main()
def print_board(game, board):
    chars = {game.none: ' ', game.x: 'X', game.o: 'O'}
    for i in range(3):
        for j in range(3):
            print(chars[board[i][j]], end='')
            if j < 2:
                print('|', end='')
        print()
        if i < 2:
            print('-----')

# Define the main() function
def main():
    agent_x = QLearningAgent()
    agent_o = QLearningAgent()

    for episode in range(10000):
        game = TicTacToe()
        current_player, other_player = game.x, game.o
        current_agent, other_agent = agent_x, agent_o

        while game.is_end() == game.none:
            old_state = game.board.copy()
            action = current_agent.choose_action(old_state, game.valid_moves())
            reward = game.make_move(current_player, *action)
            new_state = game.board.copy()

            if game.is_end() == game.none:
                next_max_q_value = np.max([current_agent.get_q_value(new_state, a) for a in game.valid_moves()])
            else:
                next_max_q_value = 0.0

            current_agent.update_q_value(old_state, action, reward, next_max_q_value)

            current_player, other_player = other_player, current_player
            current_agent, other_agent = other_agent, current_agent

        agent_x.decay_exploration_rate()
        agent_o.decay_exploration_rate()

    # After training, let's watch the agents play
    print("After training, let's watch a game:")
    game = TicTacToe()
    current_player, other_player = game.x, game.o
    current_agent, other_agent = agent_x, agent_o
    while game.is_end() == game.none:
        action = current_agent.choose_action(game.board.copy(), game.valid_moves())
        game.make_move(current_player, *action)
        print_board(game, game.board)
        print()
        current_player, other_player = other_player, current_player
        current_agent, other_agent = other_agent, current_agent

# Run the main() function
if __name__ == "__main__":
    main()
