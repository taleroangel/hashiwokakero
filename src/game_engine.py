from game_state import GameState, Bridge
import pygame
import automatic
import os
import time


class Colors:
    BACKGROUND = '#DDD7EF'
    ON_BACKGROUND = '#9386D0'

    NODES = '#B496DA'
    ON_NODES = '#000000'

    BRIDGES = '#E1B2B2'
    ON_BRIDGES = '#000000'


class GameEngine:

    # Block Size
    BLOCK_SIZE = 100
    BLOCK_CENTER = int(BLOCK_SIZE / 2)

    # Nodes
    NODE_CIRCLE_RADIUS = int(BLOCK_CENTER - (BLOCK_SIZE * 0.2))

    # Fonts
    LARGE_FONT_SIZE = int(BLOCK_SIZE * 0.4)
    SMALL_FONT_SIZE = int(BLOCK_SIZE * 0.35)

    # Bridges
    BRIDGE_WIDTH = 5
    BRIDGE_BACKGROUND_RADIUS = int(SMALL_FONT_SIZE * 0.45)

    def fromMtxToCoordinates(i, j):
        """
        Transform a pair of indexes into coordinates
        """
        return i * GameEngine.BLOCK_SIZE + GameEngine.BLOCK_CENTER, j * GameEngine.BLOCK_SIZE + GameEngine.BLOCK_CENTER

    def fromCoordinatesToMtx(coordinates: tuple):
        """
        Transform a tuple of coordinates into a pair of matrix indexes
        """
        return int(coordinates[1] / GameEngine.BLOCK_SIZE), int(coordinates[0] / GameEngine.BLOCK_SIZE)

    def __init__(self, game: GameState, playAutomatic=False) -> None:
        # Initialize pygame
        self.game = game
        pygame.init()

        self.automatic: automatic.AutomaticPlayer | None = automatic.AutomaticPlayer(
            game) if playAutomatic else None

        # Variables de pantalla
        self.screenSize = int(game.size * GameEngine.BLOCK_SIZE)

        # Inicializar Pantalla
        self.screen = pygame.display.set_mode(
            (self.screenSize, self.screenSize))

        # Set icon and caption into screen
        pygame.display.set_caption("Hashiwokakero")
        icon = pygame.image.load(os.path.join(
            os.path.dirname(__file__), '../assets/icon.svg'))
        pygame.display.set_icon(icon)

        # Crear la fuente
        self.largeFont = pygame.font.Font(None, GameEngine.LARGE_FONT_SIZE)
        self.smallFont = pygame.font.Font(None, GameEngine.SMALL_FONT_SIZE)

        # Help buttons
        print("GameEngine: press 'H' to show a list of commands")
        self._buttons = {
            pygame.K_h: ['H', "Show help", self.showHelp],
            pygame.K_r: ['R', "Restart the game", self.restartGame],
            pygame.K_n: ['N', "Show the node matrix", self.showNodesMatrix],
            pygame.K_b: ['B', "Show the bridge matrix", self.showBridgeMatrix],
            pygame.K_a: ['A', "Show the bridge list", self.showBridgeList],
        }

    def __del__(self) -> None:
        pygame.quit()

    def gameLoop(self):

        latest_play_time = 0

        # GameLoop variables
        latestClick = None

        # Event Loop de Pygame
        while True:

            # Verificar si ha ganado
            if self.game.hasWon():
                print("Congratulations!!")
                return

            # Registrar eventos
            for event in pygame.event.get():
                # Exit event
                if event.type == pygame.QUIT:
                    return

                if self.automatic is None:
                    # Mouse hold down
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        latestClick = pygame.mouse.get_pos()

                    # Mouse hold up
                    if event.type == pygame.MOUSEBUTTONUP:

                        # Transformar las coordenadas a índices de matrices
                        latestClick = GameEngine.fromCoordinatesToMtx(
                            latestClick)
                        newClick = GameEngine.fromCoordinatesToMtx(
                            pygame.mouse.get_pos())

                        # Create bridge
                        self.createNewBridge(latestClick, newClick)
                        latestClick = None

                elif time.time() - latest_play_time > 1:
                    play = self.automatic.play()

                    if play is not None:
                        self.createNewBridge(*play)
                    else:
                        print("Automatic failed to play")

                    latest_play_time = time.time()

                # Keyboard press
                if event.type == pygame.KEYDOWN:
                    try:
                        self._buttons[event.key][2]()
                    except:
                        print("Unrecognized Command")

            # Rendering
            self.screen.fill(Colors.BACKGROUND)
            self.drawLines()
            self.mouseLineHold(latestClick)
            self.drawNodes()

            # Actualizar el display
            pygame.display.update()

    def showHelp(self):
        """
        Show a help message
        """
        print("\nHelp:")
        for value in self._buttons.values():
            print(f'{value[0]}: {value[1]}')

    def showNodesMatrix(self):
        """
        Show the nodes matrix
        """
        print("\nNodes Matrix:")
        for row in self.game.nodes:
            print(row)

    def showBridgeMatrix(self):
        """
        Show the bridge matrix
        """
        print("\nBridge Matrix:")
        for row in self.game.connections:
            print(row)

    def showBridgeList(self):
        """
        Show the bridge list
        """
        print("\nBridge List:")
        if len(self.game.bridges) == 0:
            print("There are no bridges")
        else:
            for row in self.game.bridges:
                print(row)

    def restartGame(self):
        """
        Restart all game variables
        """
        print("\nRestarted game variables!")
        self.game.restart()

    def mouseLineHold(self, latestClick):
        """
        Show a line while holding the click
        """
        if latestClick != None:
            pygame.draw.line(self.screen,
                             Colors.ON_BACKGROUND,
                             latestClick,
                             pygame.mouse.get_pos(),
                             GameEngine.BRIDGE_WIDTH)

    def drawNodes(self):
        """
        Render nodes from matrix into screen
        """

        # Recorrer horizontalmente
        for i, y in enumerate(range(0, self.screenSize, GameEngine.BLOCK_SIZE)):
            # Recorrer verticalmente
            for j, x in enumerate(range(0, self.screenSize, GameEngine.BLOCK_SIZE)):
                if self.game.nodes[i][j] != 0:
                    # Mostrar el nodo
                    pygame.draw.circle(self.screen, Colors.NODES,
                                       [x + GameEngine.BLOCK_CENTER,
                                           y + GameEngine.BLOCK_CENTER],
                                       GameEngine.NODE_CIRCLE_RADIUS)
                    # Crear un texto
                    text = self.largeFont.render(
                        str(self.game.nodes[i][j]), True, Colors.ON_NODES)
                    self.screen.blit(text, [x + GameEngine.BLOCK_CENTER - text.get_width() / 2,
                                            y + GameEngine.BLOCK_CENTER - text.get_height() / 2])

    def drawLines(self):
        """
        Render bridges into screens
        """

        for bridge in self.game.bridges:
            # Dibujar la línea
            line = pygame.draw.line(self.screen, Colors.BRIDGES,
                                    GameEngine.fromMtxToCoordinates(
                                        bridge.origin[1], bridge.origin[0]),
                                    GameEngine.fromMtxToCoordinates(
                                        bridge.destination[1], bridge.destination[0]),
                                    GameEngine.BRIDGE_WIDTH
                                    )

            # Crear un círculo de fondo
            pygame.draw.circle(self.screen, Colors.BRIDGES,
                               line.center, GameEngine.BRIDGE_BACKGROUND_RADIUS)

            # Crear un texto indicador de peso
            text = self.smallFont.render(
                str(bridge.weight), True, Colors.ON_BRIDGES)
            self.screen.blit(text, [line.center[0] - text.get_width() / 2,
                                    line.center[1] - text.get_height() / 2])

    def createNewBridge(self, latestClick, newClick):
        # Calcular la nueva línea
        try:
            # Crear la nueba línea
            self.game.addBridge(latestClick, newClick)
        except ValueError as e:
            print(f"\nBridgeError: {e.args[0]}")
        except RuntimeWarning as e:
            print(f"\nBridgeWarning: {e.args[0]}")
