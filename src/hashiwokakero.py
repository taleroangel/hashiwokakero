def hashiwokakero(input: str, automatic: bool):
    """
    Start a new game
    """

    # Crear el estado del juego
    from game_state import GameState
    game = GameState(input)

    # Crear el motor de juego
    from game_engine import GameEngine
    engine = GameEngine(game, automatic)
    
    # Iniciar el juego
    engine.gameLoop()
