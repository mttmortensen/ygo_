# ygo_
# Yu-Gi-Oh! Duel Simulator for Machine Learning
This project is a simplified version of the popular trading card game, Yu-Gi-Oh!, designed specifically for training machine learning models. The game focuses on Normal and Tribute Summons, and only uses Normal type monsters.

## Game Mechanics
The game simulates a duel between two players, each starting with 8000 Life Points. Players take turns drawing cards from their decks, summoning monsters to the field, and attacking their opponent's monsters or directly attacking their opponent's Life Points.

The game includes the following mechanics:

- **Normal Summon**: Players can summon a Level 4 or lower monster from their hand to the field in Attack or Defense position.
- **Tribute Summon**: Players can summon a Level 5 or higher monster from their hand to the field by tributing one or two monsters they control, depending on the Level of the monster being summoned.
- **Battle**: Monsters can attack other monsters or directly attack the opponent's Life Points. The outcome of a battle depends on the Attack and Defense points of the monsters involved.

## Machine Learning Model
The goal of the machine learning model is to learn to play the game effectively by choosing the most consistent and powerful Normal monsters for a duel. The model is trained using reinforcement learning, with the game state as the state space and the possible actions as the action space.

The reward function is designed to encourage the model to reduce the opponent's Life Points and to penalize it for losing its own Life Points. The model also receives a large reward for winning the game and a large penalty for losing the game.

## Future Work
Future updates to this project may include additional game mechanics, such as Spell and Trap Cards, and more complex monster effects. The machine learning model may also be extended to learn more complex strategies and to adapt to different game situations.
