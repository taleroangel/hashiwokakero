import game_state as gs
import random


class AutomaticPlayer:

    def __init__(self, game: gs.GameState) -> None:
        print("AutomaticPlayer is playing...")
        self.game = game

    def play(self) -> gs.CoordinatesTuple:

        print('\n')

        # Jugar las heurísticas
        heuristics = self.play_heuristics()
        if heuristics is not None:
            print(f"Automatic plays [Heuristic]: {heuristics}")
            return heuristics

        # Si no hay una heurística para jugar
        else:
            # TODO: Hacer otras jugadas (Fuerza bruta?)
            print(f"Automatic plays [?]: {None}")
            return None

    # --- HEURISTICAS ---
    # HEURISTICAS: https://www.hashi.info/how-to-solve

    def play_heuristics(self):
        """
        Jugar todas las heurísticas
        """
        rule = self.one_way_connection_heuristic()
        if rule is not None:
            print("[Heuristic] = OneWayConnection")
            return rule

        # Play rule of number 8 and rule of number 7
        rule = self.number_7_8_heuristic()
        if rule is not None:
            print("[Heuristic] = Number7/8")
            return rule

        return None

    def one_way_connection_heuristic(self):
        """
        Cuando sólo se tiene un vecino, esa es la única posible jugada
        y por lo tanto debe jugarse
        """

        for idx, rows in enumerate(self.game.nodes):
            for jdx, node in enumerate(rows):

                origin = (idx, jdx)

                # Calculate number of nodes
                n_nodes = self.game.numberOfNeightbors(origin)

                # If exactly one
                if n_nodes == 1:
                    # Get the neightbor
                    destination = self.game.findNeightbor(origin)

                    # Get bridges
                    if self.game.checkBridgeWeight(origin, destination) < min(
                        node, self.game.nodes[destination[0]][destination[1]],
                    ):
                        return (origin, destination)

        return None

    def number_7_8_heuristic(self) -> gs.CoordinatesTuple | None:
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
