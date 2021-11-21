import cv2
import numpy as np

class Minigame:
    def __init__(self, pygame, screen, clock, hasCustomEvent=False):
        self.pygame = pygame
        self.screen = screen
        self.clock = clock
        self.hasCustomEvent = hasCustomEvent
        
        self.size = screen.get_size()

    def apply_blooming(self, surface) -> np.ndarray:
        # Provide some blurring to image, to create some bloom.
        #image = self.pygame.transform.scale(surface,(self.size[0]*1.5, self.size[1]*1.5)) 
        image = self.pygame.surfarray.array3d(surface)
        cv2.GaussianBlur(image, ksize=(15, 15), sigmaX=10, sigmaY=10, dst=image)
        cv2.blur(image, ksize=(30, 30), dst=image)

        image = self.pygame.surfarray.make_surface(image)
        #image = self.pygame.transform.scale(image,self.size)
        return image

    def draw(self, color: tuple, dimensions: tuple):
        self.pygame.draw.rect(self.screen, color, dimensions,0)

    def vw(self, percent): #viewport width
        return percent/100 * self.size[0]
    def vh(self, percent): #viewport height
        return percent/100 * self.size[1]

    def drawLine(self, color, pos, w):
         self.pygame.draw.aalines(self.screen, color, False, pos, w)

    def drawImage(self, img, pos: tuple):
        self.screen.blit(img, pos)

    def drawTransparentRect(self,color: tuple, size: tuple, pos: tuple):
        s = self.pygame.Surface(size, self.pygame.SRCALPHA)   # per-pixel alpha
        s.fill(color)                         # notice the alpha value in the color
        self.screen.blit(s, pos)

    def renderText(self, text, pos, color, fontSize=24,centerAndBoxSize=False):
        font = self.pygame.freetype.Font("SourceSansPro-Regular.ttf", fontSize)
        
        textRect = font.render(text)[1]

        if centerAndBoxSize != False:
            #WtextRect = text.get_rect(text)
            newPos = list(pos)
            newPos[0] = newPos[0] + centerAndBoxSize[0]/2 - textRect.width/2
            newPos[1] = newPos[1] + centerAndBoxSize[1]/2 - textRect.height/2
            font.render_to(self.screen, newPos, text, color)
            return
        
        font.render_to(self.screen, pos, text, color)

        return textRect

    
    def run(self):
        self.draw((0,0,0), (0,0, 50,50))
    
    def stop(self):
        pass