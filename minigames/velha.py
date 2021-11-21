from .game import Minigame

class Velha(Minigame):
    def __init__(self, pygame, screen, clock):
        super().__init__(pygame, screen, clock)

    def run(self):
        self.draw((0,0,0), (50,50, 50,50))
    