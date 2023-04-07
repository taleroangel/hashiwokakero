class Bridge:
    def __init__(self, mtx, origin: tuple, destination: tuple, weight: int) -> None:

        # Verificar que no sea el mismo
        if origin == destination:
            raise ValueError("No puede ser igual el origen que el destino")

        # Verificar el peso de los puentes
        if mtx[origin[0]][origin[1]] < weight:
            raise ValueError("El origen no puede soportar este puente")
        if mtx[destination[0]][destination[1]] < weight:
            raise ValueError("El destino no puede soportar este puente")

        # Verificar que no sean diagonales
        if not (origin[0] == destination[0] or origin[1] == destination[1]):
            raise ValueError("No pueden usarse diagonales")

        # Verificar que no pase por encima de otro nodo
        isHorizontal = (origin[0] == destination[0])
        if isHorizontal:
            start = min(origin[1], destination[1]) + 1
            stop = max(origin[1], destination[1])

            isValid = True
            for step in range(start, stop):
                if mtx[origin[0]][step] != 0:
                    isValid = False

            if not isValid:
                raise ValueError("Se cruzan nodos")

        else:
            start = min(origin[0], destination[0]) + 1
            stop = max(origin[0], destination[0])

            isValid = True
            for step in range(start, stop):
                if mtx[step][origin[1]] != 0:
                    isValid = False

            if not isValid:
                raise ValueError("Se cruzan nodos")

        # Asignar variables
        self.origin = origin
        self.destination = destination
        self.weight = weight


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
            assert size[0] == size[1]
            self.size = int(size[0])

            # Obtener el resto de líneas
            self.nodes = []

            i = 0  # Contador de columna
            for row in lines[1:]:
                self.nodes.append([])  # Agregar una nueva fila
                for item in row:  # Agregar cada elemento
                    self.nodes[i].append(int(item))
                i += 1  # Siguiente columna

            # Crear la matrix de puentes vacía
            self.bridges = []

    # end __init__

    def addBridge(bridge: Bridge):
        pass

    def removeBridge(bridge: Bridge):
        pass
