from game_state import GameState, Bridge
from game_engine import GameEngine

# Crear el estado del juego
game = GameState('input.in')

# Print nodes
print("Nodes:")
for row in game.nodes:
    print(row)

# Crear el motor de juego
engine = GameEngine(game)
engine.gameLoop()
