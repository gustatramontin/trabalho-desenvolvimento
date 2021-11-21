from numpy.core.fromnumeric import shape
from .game import Minigame
import numpy as np

import cv2
import mediapipe as mp
import numpy as np

import pickle

class Shapes(Minigame):
    def __init__(self, pygame, screen, clock):
        super().__init__(pygame, screen, clock)
        self.direction = None
        self.size = screen.get_size()

        self.drawing = False

        self.sub_canvas = []
        self.canvas = []

        self.pencil_size = 10


        
    def run(self, key, mouse):
        if key != None:
            self.handleKey(key)


        if mouse != None:
            self.handleMouse(mouse)

        self.drawPaint()

    def handleKey(self, key):
        if key == 'r':
            self.canvas = []
            self.sub_canvas = []

        if key == 'a':
            self.drawing = True

        if key == 's':
            self.drawing = False

    def handleMouse(self, pos):
        
        if self.drawing:
            self.sub_canvas.append((pos[0], pos[1], (0,0,0)))
            print(self.canvas)
        elif len(self.sub_canvas) > 0:
            self.canvas.append((self.sub_canvas))
            self.sub_canvas = []

    def drawPaint(self):
        
        self.drawTransparentRect((255,255,255,255),(self.size[0],self.size[1]), (0,0))

        if len(self.sub_canvas) > 1:
            self.drawLine((0,0,0), np.array(self.sub_canvas)[:, :-1], 15)
            self.drawLine((0,0,0), np.array(self.sub_canvas)[:, :-1]+0.5, 15)
            self.drawLine((0,0,0), np.array(self.sub_canvas)[:, :-1]-0.5, 15)


        if len(self.canvas) > 1 and len(self.canvas[0]) > 1:
            for line in self.canvas:
                if len(line) > 1:
                    self.drawLine((0,0,0), np.array(line)[:, :-1], 15)
                    self.drawLine((0,0,0), np.array(line)[:, :-1]+0.5, 15)
                    self.drawLine((0,0,0), np.array(line)[:, :-1]-0.5, 15)
            #self.draw(point[2], (point[0], point[1], self.pencil_size, self.pencil_size))

    def stop(self):
        pass

    