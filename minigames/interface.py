from .game import Minigame
import pygame.freetype
from time import process_time, sleep

class Button:
    def __init__(self, size, text, click):
        self.size = size
        self.text = text
        self.click = click

    def checkClick(self, pos):
        insideX = (pos[0] > self.size[0] and pos[0] < self.size[0] + self.size[2])
        insideY = (pos[1] > self.size[1] and pos[1] < self.size[1] + self.size[3])

        if insideX and insideY:
            self.click("snake")

    def run(self, key, mouse, draw, renderText):
        draw((255,0,0), self.size)
        renderText(self.text, (self.size[0], self.size[1]), 
                    (255,255,255), 
                    (self.size[2], self.size[3])
        )


class Interface(Minigame):
    def __init__(self, pygame, screen, clock, switch_game):
        super().__init__(pygame, screen, clock, hasCustomEvent=True)

        self.switch_game = switch_game

        self.buttons = []
        self.buttonSize = (100,50)
        self.buttonPos = (self.vw(50) - self.buttonSize[0]/2, self.vh(50) - self.buttonSize[1]/2)
        self.buttons.append(Button((self.buttonPos[0],self.buttonPos[1], 
                                    self.buttonSize[0],self.buttonSize[1]),
                                    "Play", self.switch_game))
        self.texts = ["Welcome to Jeux Video", "Type help to see a list of commands"]
        self.prompt = ""
        self.printState = 0

        self.minigames = ['snake', 'obstacles', 'shapes']
    
    def renderTexts(self):
        fontSize = 20
        padding = 12
        initialPos = (10,10)

        numberOfLetters = 0

        for text in self.texts:
            numberOfLetters += len(text)

        for t in range(1, len(self.texts)): 
            for l in range(1, len(list(self.texts[t]))):
                pass
            
        textRect = self.renderText(self.texts[0], (10,10), (0,255,0), fontSize)
        

        for i in range(1, len(self.texts)): 
            self.renderText(self.texts[i], (10, 10 + i*(textRect.height + padding)) , (0,255,0), fontSize)

        self.renderText(f"[jeux@video]$ {self.prompt}", (10, 10 + len(self.texts) * (textRect.height + padding)), (0,255,0), fontSize)

    def run(self, key, mouse):

        self.draw((0,0,0), (0,0, self.size[0],self.size[1]))
        """self.renderText("Type s to play snake", (11,11), (0,150,0))
        textRect = self.renderText("Type s to play snake", (10,10), (0,255,0))
        self.renderText(f"> {self.prompt}", (10,10 + textRect.height + 10), (0,255,0))"""

        self.renderTexts()

        surface = self.pygame.display.get_surface()#surfarray.array3d(self.screen)
        surface = self.apply_blooming(surface)
        #img = self.pygame.surfarray.make_surface(surface)
        centerY = self.size[1]*1.5-self.size[1]
        print(centerY, self.size[1]*1.5)
        self.screen.blit(surface, (0,0))

        self.renderTexts()

        if key and key not in ["return", "backspace"] and len(key) == 1:
            self.prompt += key
        
        if key == "return":
            
            self.texts.append(f"[jeux@video]$ {self.prompt}")
    
            if self.prompt in self.minigames:
                self.switch_game(self.prompt)
                self.texts.append(f"Playing {self.prompt}")

            elif self.prompt == "clear":
                self.texts = self.texts[0:2]
            elif self.prompt == "help":
                self.texts.append("clear - help - snake - obstacles")
            else:
                self.texts.append("Command Invalid")
            
            self.prompt = ""

        elif key == "backspace":
            self.prompt = "".join(list(self.prompt)[:-1])

            #self.texts.append(self.prompt)
        #for b in self.buttons:
         #   b.run(key, mouse, self.draw, self.renderText)

    def customEvent(self, event):
        if event.type == self.pygame.MOUSEBUTTONUP:
            for b in self.buttons:
                b.checkClick(self.pygame.mouse.get_pos())
