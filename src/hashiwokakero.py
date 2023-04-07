def hashiwokakero(input):
    """
    Start a new game
    """

    # Crear el estado del juego
    from game_state import GameState
    game = GameState(input)

    # Crear el motor de juego
    from game_engine import GameEngine
    engine = GameEngine(game)
    
    # Iniciar el juego
    engine.gameLoop()
