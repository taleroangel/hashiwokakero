from typing import Callable

CoordinatesTuple = tuple[tuple[int, int], tuple[int, int]]


class GameState:
    def __init__(self, filename: str) -> None:
        """
        Lee el archivo 'filename' y genera las variables de juego
        """

        with open(filename, 'r') as file:
            # Leer las líneas
            lines = file.readlines()

            # Quitarles los EOL
            lines = list(map(lambda x: x.replace(
                '\n', '').replace('\r', ''), lines))

            # Obtener y guardar el tamaño, (debe ser cuadrado nxn)
            size = lines[0].split(',')
            assert size[0] == size[1], "Matriz is not squared"
            self.size = int(size[0])

            # Obtener el resto de líneas
            self.nodes = []

            # Crear la matrix de conexiones vacía
            self.connections = [
                [0 for _ in range(self.size)] for _ in range(self.size)]

            for i, row in enumerate(lines[1:]):
                # Agregar una nueva fila
                self.nodes.append([])

                # For each item in row
                for item in row:
                    # Agregar cada elemento
                    self.nodes[i].append(int(item))
                    assert int(item) <= 8

            # Crear la lista de puentes vacía
            self.bridges = []

    def restart(self):
        self.bridges = []
        self.connections = [
            [0 for _ in range(self.size)] for _ in range(self.size)]

    def hasWon(self) -> bool:
        for i, row in enumerate(self.nodes):
            for j, item in enumerate(row):
                if (item != 0) and (item != self.connections[i][j]):
                    return False
        return True

    def checkBridgeWeight(
        self,
        origin: CoordinatesTuple,
        destination: CoordinatesTuple
    ) -> int:
        """
        Verificar cuántos puentes hay entre origen y destino
        """

        for bridge in self.bridges:
            if ((bridge.origin == origin and bridge.destination == destination) or
                    (bridge.destination == origin and bridge.origin == destination)):
                return bridge.weight

        return 0

    def addBridge(self, origin, destination):
        self.bridges.append(Bridge(self, origin, destination))

    def findNeightbor(
            self,
            origin: CoordinatesTuple,
            conditional: Callable[[CoordinatesTuple], bool] = lambda _: True
    ) -> CoordinatesTuple:
        """
        Retona las coordenadas del primer vecino encontrado en cualquier dirección
        desde un origen, recibe un callback como condicional para evaluar el
        vecino a retornar
        """

        idx, jdx = origin

        # Right
        for k in range(jdx + 1, self.size):
            if self.nodes[idx][k] > 0:
                if conditional((idx, k)):
                    return (idx, k)
                else:
                    break

        # Top
        for k in range(idx + 1, self.size):
            if self.nodes[k][jdx] > 0:
                if conditional((k, jdx)):
                    return (k, jdx)
                else:
                    break

        # Left
        for k in range(jdx - 1, -1, -1):
            if self.nodes[idx][k] > 0:
                if conditional((idx, k)):
                    return (idx, k)
                else:
                    break

        # Bottom
        for k in range(idx - 1, -1, -1):
            if self.nodes[k][jdx] > 0:
                if conditional((k, jdx)):
                    return (k, jdx)
                else:
                    break

        return None

    def findNeightborConsiderBridges(
            self,
            origin: CoordinatesTuple,
            conditional: Callable[[CoordinatesTuple], bool] = lambda _: True
    ) -> CoordinatesTuple:
        """
        Retona las coordenadas del primer vecino encontrado en cualquier dirección
        que sea alcanzable dado que no hay puentes en el camino
        desde un origen, recibe un callback como condicional para evaluar el
        vecino a retornar
        """

        idx, jdx = origin

        # Right
        for k in range(jdx + 1, self.size):
            if self.connections[idx][k] > 0 and self.nodes[idx][k] == 0:
                break
            if self.nodes[idx][k] > 0:
                if conditional((idx, k)):
                    return (idx, k)
                else:
                    break

        # Top
        for k in range(idx + 1, self.size):
            if self.connections[k][jdx] > 0 and self.nodes[k][jdx] == 0:
                break
            if self.nodes[k][jdx] > 0:
                if conditional((k, jdx)):
                    return (k, jdx)
                else:
                    break

        # Left
        for k in range(jdx - 1, -1, -1):
            if self.connections[idx][k] > 0 and self.nodes[idx][k] == 0:
                break
            if self.nodes[idx][k] > 0:
                if conditional((idx, k)):
                    return (idx, k)
                else:
                    break

        # Bottom
        for k in range(idx - 1, -1, -1):
            if self.connections[k][jdx] > 0 and self.nodes[k][jdx] == 0:
                break
            if self.nodes[k][jdx] > 0:
                if conditional((k, jdx)):
                    return (k, jdx)
                else:
                    break

        return None

    def numberOfNeightbors(
            self,
            origin: CoordinatesTuple,
    ) -> int:
        """
        Retona el numero de vecinos de un nodo
        """

        idx, jdx = origin
        n_nodes = 0

        # Right
        for k in range(jdx + 1, self.size):
            if self.nodes[idx][k] > 0:
                n_nodes += 1
                break

        # Top
        for k in range(idx + 1, self.size):
            if self.nodes[k][jdx] > 0:
                n_nodes += 1
                break

        # Left
        for k in range(jdx - 1, -1, -1):
            if self.nodes[idx][k] > 0:
                n_nodes += 1
                break

        # Bottom
        for k in range(idx - 1, -1, -1):
            if self.nodes[k][jdx] > 0:
                n_nodes += 1
                break

        return n_nodes

    def numberOfNeightborsConsiderBridges(
            self,
            origin: CoordinatesTuple
    ) -> int:

        idx, jdx = origin
        n_nodes = 0

        # Right
        for k in range(jdx + 1, self.size):
            if self.connections[idx][k] > 0 and self.nodes[idx][k] == 0:
                break
            if self.nodes[idx][k] > 0:
                n_nodes += 1
                break

        # Top
        for k in range(idx + 1, self.size):
            if self.connections[k][jdx] > 0 and self.nodes[k][jdx] == 0:
                break
            if self.nodes[k][jdx] > 0:
                n_nodes += 1
                break

        # Left
        for k in range(jdx - 1, -1, -1):
            if self.connections[idx][k] > 0 and self.nodes[idx][k] == 0:
                break
            if self.nodes[idx][k] > 0:
                n_nodes += 1
                break

        # Bottom
        for k in range(idx - 1, -1, -1):
            if self.connections[k][jdx] > 0 and self.nodes[k][jdx] == 0:
                break
            if self.nodes[k][jdx] > 0:
                n_nodes += 1
                break

        return n_nodes


class Bridge:
    BRIDGE_HARD_LIMIT = 2

    def __init__(self, game: GameState, origin: tuple, destination: tuple) -> None:
        # Asignar variables
        self.game = game  # Associated game state
        self.origin = origin  # Origin node
        self.destination = destination  # Destination node

        self.weight = 1  # Number of bridges or weight
        self.wasInit = False  # Initializatoin failure

        # 1. Verificar que no sea el mismo
        if origin == destination:
            raise ValueError("Origin equal to Destination")

        # 2. Verificar que no sean diagonales
        if not ((origin[0] == destination[0]) or (origin[1] == destination[1])):
            raise ValueError("Cannot be a diagonal")

        # 3.2. Verificar el peso de los puentes
        if ((game.connections[origin[0]][origin[1]] >= game.nodes[origin[0]][origin[1]]) or
                (game.connections[destination[0]][destination[1]] >= game.nodes[destination[0]][destination[1]])):
            # Verificar si ya existe y eliminarlo
            if (self in self.game.bridges):
                self.game.bridges.remove(self)
                raise RuntimeWarning(
                    "Removed existing bridge, exceeded node value")
            # No puede exceder el valor
            raise ValueError("Number of bridges cannot exceed node value")

        # 4. Verificar si ya existe el nodo
        if (self in self.game.bridges):
            bridge = self.game.bridges[self.game.bridges.index(self)]

            if bridge.weight >= Bridge.BRIDGE_HARD_LIMIT:
                self.game.bridges.remove(self)
                raise RuntimeWarning(
                    "Removed existing bridge, exceeded node value")
            else:
                bridge.weight += 1
                bridge.alterSteps()
                bridge.addOneToNode()
                raise RuntimeWarning("Bridge updated")

        # 5. Verificar si pasa por encima de otros nodos o puentes
        isHorizontal = (origin[0] == destination[0])
        axisIndex = 1 if isHorizontal else 0
        commonAxis = origin[0] if isHorizontal else origin[1]

        # Start end Stop index
        start = min(origin[axisIndex], destination[axisIndex]) + 1
        stop = max(origin[axisIndex], destination[axisIndex])

        # Calculate slices
        for step in range(start, stop):
            # Check if placing on top of a node
            if game.nodes[commonAxis if isHorizontal else step][step if isHorizontal else commonAxis] != 0:
                raise ValueError("Cannot place a bridge on top of a node")
                # Create the connection slie
            if game.connections[commonAxis if isHorizontal else step][step if isHorizontal else commonAxis] != 0:
                raise ValueError("Cannot place a bridge on top of another")

        # Modify value in matrix
        self.alterSteps()
        self.addOneToNode()
        self.wasInit = True

    def __del__(self):
        if self.wasInit:
            self.removeBridgeFromNodes()
            self.weight = 0
            self.alterSteps()

    def __eq__(self, __value: object) -> bool:
        return (isinstance(__value, Bridge) and
                ((self.origin == __value.origin) and
                (self.destination == __value.destination)) or
                ((self.origin == __value.destination) and
                (self.destination == __value.origin)))

    def __str__(self) -> str:
        return f'({self.origin}) ({self.destination}) ({self.weight})'

    def addOneToNode(self):
        """
        Add bridge to the total number of bridges connected to a node
        """
        self.game.connections[self.origin[0]][self.origin[1]] += 1
        self.game.connections[self.destination[0]][self.destination[1]] += 1

    def removeOneFromNodes(self):
        """
        Remove bridge from the total number of bridges connected to a node
        """
        self.game.connections[self.origin[0]][self.origin[1]] -= 1
        self.game.connections[self.destination[0]
                              ][self.destination[1]] -= 1

    def removeBridgeFromNodes(self):
        """
        Remove bridge from the total number of bridges connected to a node
        """
        self.game.connections[self.origin[0]][self.origin[1]] -= self.weight
        self.game.connections[self.destination[0]
                              ][self.destination[1]] -= self.weight

    def alterSteps(self):
        # 4. Verificar si el puente ya existe o pasa por encima de otros nodos
        isHorizontal = (self.origin[0] == self.destination[0])
        axisIndex = 1 if isHorizontal else 0
        commonAxis = self.origin[0] if isHorizontal else self.origin[1]

        # Start end Stop index
        start = min(self.origin[axisIndex], self.destination[axisIndex]) + 1
        stop = max(self.origin[axisIndex], self.destination[axisIndex])

        for step in range(start, stop):
            self.game.connections[commonAxis if isHorizontal else step][step if isHorizontal else commonAxis] = self.weight
