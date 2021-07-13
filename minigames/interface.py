from .game import Minigame

class Interface(Minigame):
    def __init__(self, pygame, screen, clock):
        super().__init__(pygame, screen, clock)

    def run(self):
        self.draw((255,0,0), (0,0, 50,50))
    