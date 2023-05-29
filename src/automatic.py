import game_state
import random


class AutomaticPlayer:

    def __init__(self, game: game_state.GameState) -> None:
        print("AutomaticPlayer is playing...")
        self.game = game

    def play(self) -> tuple[tuple[int, int], tuple[int, int]]:
        
        

        fromt = (x1, y1)
        tot = (x2, y2)

        print(f"Random plays: {fromt} {tot}")
        return fromt, tot
