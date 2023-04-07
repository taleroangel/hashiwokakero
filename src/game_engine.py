from game_state import GameState, Bridge
import pygame


class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255),
    BLUE = (0, 0, 255),
    RED = (255, 0, 0)


class GameEngine:

    # Colores
    SCREEN_BLOCK_SIZE = 100
    BLOCK_CENTER = int(SCREEN_BLOCK_SIZE / 2)

    NODE_CIRCLE_RADIUS = BLOCK_CENTER - (SCREEN_BLOCK_SIZE * 0.1)

    LINE_WIDTH = 5
    LARGE_FONT_SIZE = int(SCREEN_BLOCK_SIZE * 0.5)
    SMALL_FONT_SIZE = int(SCREEN_BLOCK_SIZE * 0.4)
    TEXT_BACKGROUND_RADIUS = int(SMALL_FONT_SIZE * 0.45)

    def __init__(self, game: GameState) -> None:
        # GameState
        self.game = game

        # Inicializar PyGame
        pygame.init()

        # Variables de pantalla
        self.screenSize = int(game.size * GameEngine.SCREEN_BLOCK_SIZE)

        # Inicializar Pantalla
        self.screen = pygame.display.set_mode(
            (self.screenSize, self.screenSize))

        # Crear la fuente
        self.largeFont = pygame.font.Font(None, GameEngine.LARGE_FONT_SIZE)
        self.smallFont = pygame.font.Font(None, GameEngine.SMALL_FONT_SIZE)

    def gameLoop(self):
        # Event Loop de Pygame
        latestClick = None

        while True:
            # Registrar eventos
            for event in pygame.event.get():
                # Exit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    latestClick = GameEngine.fromCoordinatesToMtx(
                        pygame.mouse.get_pos())

                if event.type == pygame.MOUSEBUTTONUP:
                    newClick = GameEngine.fromCoordinatesToMtx(
                        pygame.mouse.get_pos())

                    # Calcular la nueva línea
                    try:
                        self.game.bridges.append(
                            Bridge(self.game.nodes, latestClick, newClick, 1)
                        )
                    except ValueError as e:
                        print(f"No válido: {e.args[0]}")
                    finally:
                        latestClick = None

            self.screen.fill(Colors.BLACK)
            self.drawLines()
            self.drawNodes()

            # Actualizar el display
            pygame.display.update()

    def fromMtxToCoordinates(i, j):
        return i * GameEngine.SCREEN_BLOCK_SIZE + GameEngine.BLOCK_CENTER, j * GameEngine.SCREEN_BLOCK_SIZE + GameEngine.BLOCK_CENTER

    def fromCoordinatesToMtx(coordinates: tuple):
        return int(coordinates[1] / GameEngine.SCREEN_BLOCK_SIZE), int(coordinates[0] / GameEngine.SCREEN_BLOCK_SIZE)

    def drawNodes(self):
        i = 0
        # Recorrer horizontalmente
        for y in range(0, self.screenSize, GameEngine.SCREEN_BLOCK_SIZE):
            j = 0
            # Recorrer verticalmente
            for x in range(0, self.screenSize, GameEngine.SCREEN_BLOCK_SIZE):
                if self.game.nodes[i][j] != 0:
                    # Mostrar el nodo
                    pygame.draw.circle(self.screen, Colors.WHITE,
                                       [x + GameEngine.BLOCK_CENTER,
                                        y + GameEngine.BLOCK_CENTER],
                                       GameEngine.NODE_CIRCLE_RADIUS, 0)
                    # Crear un texto
                    text = self.largeFont.render(
                        str(self.game.nodes[i][j]), True, Colors.BLACK)
                    self.screen.blit(text, [x + GameEngine.BLOCK_CENTER - text.get_width() / 2,
                                            y + GameEngine.BLOCK_CENTER - text.get_height() / 2])
                j += 1  # Aumentar la columnas
            i += 1  # Aumentar las filas

    def drawLines(self):
        for bridge in self.game.bridges:
            line = pygame.draw.line(self.screen, Colors.BLUE,
                                    GameEngine.fromMtxToCoordinates(
                                        bridge.origin[1], bridge.origin[0]),
                                    GameEngine.fromMtxToCoordinates(
                                        bridge.destination[1], bridge.destination[0]),
                                    GameEngine.LINE_WIDTH
                                    )

            # Crear una bolita de fondo
            pygame.draw.circle(self.screen, Colors.BLUE,
                               line.center, GameEngine.TEXT_BACKGROUND_RADIUS)

            # Crear un texto
            text = self.smallFont.render(
                str(bridge.weight), True, Colors.WHITE)
            self.screen.blit(text, [line.center[0] - text.get_width() / 2,
                                    line.center[1] - text.get_height() / 2])
