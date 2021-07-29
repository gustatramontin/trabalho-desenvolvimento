
class Minigame:
    def __init__(self, pygame, screen, clock):
        self.pygame = pygame
        self.screen = screen
        self.clock = clock

    def draw(self, color: tuple, dimensions: tuple):
        self.pygame.draw.rect(self.screen, color, dimensions,0)

    def drawLine(self, color, pos, w):
         self.pygame.draw.aalines(self.screen, color, False, pos, w)

    def drawImage(self, img, pos: tuple):
        self.screen.blit(img, pos)

    def drawTransparentRect(self,color: tuple, size: tuple, pos: tuple):
        s = self.pygame.Surface(size, self.pygame.SRCALPHA)   # per-pixel alpha
        s.fill(color)                         # notice the alpha value in the color
        self.screen.blit(s, pos)
    
    def run(self):
        self.draw((0,0,0), (0,0, 50,50))
    
    def stop(self):
        pass