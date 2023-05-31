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
            bruteforce = self.play_bruteforce()
            if bruteforce is not None:
                print(f"Automatic plays [?]: {bruteforce}")
                return bruteforce

    # --- HEURISTICAS ---
    # HEURISTICAS: https://www.hashi.info/how-to-solve

    def play_heuristics(self) -> gs.CoordinatesTuple | None:
        for idx, rows in enumerate(self.game.nodes):
            for jdx, node in enumerate(rows):

                # Create origin
                origin = (idx, jdx)

                # * --- ONE WAY CONNECTION --- * #

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
                        print(f'[Heuristic] OneWayConnection')
                        return (origin, destination)

                # * --- Do Not Connect Islands Of One Between themselves -- * #

                if node == 1:
                    n_nodes_valid = self.game.numberOfNeightborsConsiderBridges(
                        origin, conditional=lambda x: self.game.nodes[x[0]][x[1]] > 1)

                    if n_nodes_valid == 1:
                        destination = self.game.findNeightborConsiderBridges(
                            origin, conditional=lambda x: self.game.nodes[x[0]][x[1]] > 1
                        )

                        print(
                            f'[Heuristic] DoNotConnectIslandsOf1BetweenThemselves')
                        return (origin, destination[0])


                # * --- FOUND 8 NODE --- * #

                # Found Eight
                if node == 8:
                    destination = self.game.findNeightbor(
                        origin, lambda x: self.game.checkBridgeWeight(origin, x) < 2)

                    if destination is not None:
                        print(f'[Heuristic] 8Rule')
                        return (origin, destination)

                # * --- FOUND 7 NODE --- * #

                # Found Seven
                if node == 7:
                    destination = self.game.findNeightbor(
                        origin, lambda x: self.game.checkBridgeWeight(origin, x) < 1)

                    if destination is not None:
                        print(f'[Heuristic] 7Rule')
                        return (origin, destination)

                # * --- ONE ONE CONNECTION (CONSIDER BRIDGES) --- * #

                # Calculate number of nodes
                n_nodes = self.game.numberOfNeightborsConsiderBridges(origin)

                # If exactly one
                if n_nodes == 1:
                    # Get the neightbor
                    destination = self.game.findNeightborConsiderBridges(
                        origin)

                    # Get bridges
                    if self.game.checkBridgeWeight(origin, destination[0]) < min(
                        node, self.game.nodes[destination[0][0]][destination[0][1]],
                    ):
                        print(f'[Heuristic] OneOneConnectionConsiderBridges')
                        return (origin, destination[0])





        print(f'No [Heuristic] found')
        return None

    def play_bruteforce(self) -> gs.CoordinatesTuple | None:
        for idx, rows in enumerate(self.game.nodes):
            for jdx, node in enumerate(rows):
                origin = (idx, jdx)

                # Calculate number of nodes
                n_nodes = self.game.numberOfNeightbors(origin)
                if n_nodes == node:
                    destinations = self.game.findNeightborConsiderBridges(origin)
                    if destinations is not None:
                        if len(destinations) == node:
                            for destination in destinations:
                                print(f'[Bruteforce] CompleteConnections')
                                return (origin, destination)