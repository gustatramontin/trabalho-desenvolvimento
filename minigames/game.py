
class Minigame:
    def __init__(self, pygame, screen, clock):
        self.pygame = pygame
        self.screen = screen
        self.clock = clock

    def draw(self, color: tuple, dimensions: tuple):
        self.pygame.draw.rect(self.screen, color, dimensions,0)

    def run(self):
        self.draw((0,0,0), (0,0, 50,50))