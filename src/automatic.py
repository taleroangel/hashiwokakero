import game_state
import random


class AutomaticPlayer:

    def __init__(self, game: game_state.GameState) -> None:
        print("AutomaticPlayer is playing...")
        self.game = game

    def play(self) -> tuple[tuple[int, int], tuple[int, int]]:

        # Jugar las heurísticas
        heuristics = self.play_heuristics()
        if heuristics is not None:
            return heuristics
        
        # Si no hay una heurística para jugar
        else:
            # TODO: Hacer otras jugadas (Fuerza bruta?)
            return None

    # --- HEURISTICAS ---
    # HEURISTICAS: https://www.hashi.info/how-to-solve

    def play_heuristics(self):
        """
        Jugar todas las heurísticas
        """

        # Play rule of number 8 and rule of number 7
        rule = self.number_7_8_rule()
        if rule is not None:
            return rule

        return None

    def number_7_8_rule(self) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """
        Si hay un 8, entonces todos sus puentes están al máximo
        Si hay un 7, hay al menos un puente en cada lado
        """

        for idx, rows in enumerate(self.game.nodes):
            for jdx, node in enumerate(rows):

                # Create origin
                origin = (idx, jdx)

                # Found Eight
                if node == 8:
                    destination = self.game.findNeightbor(
                        origin, lambda x: self.game.checkBridgeWeight(origin, x) < 2)

                    if destination is not None:
                        return (origin, destination)

                # Found Seven
                if node == 7:
                    destination = self.game.findNeightbor(
                        origin, lambda x: self.game.checkBridgeWeight(origin, x) < 1)

                    if destination is not None:
                        return (origin, destination)

        return None
