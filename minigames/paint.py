from numpy.core.fromnumeric import shape
from .game import Minigame
import numpy as np

import cv2
import mediapipe as mp
import numpy as np

import pickle

class Paint(Minigame):
    def __init__(self, pygame, screen, clock, cap):
        super().__init__(pygame, screen, clock)
        self.direction = None
        self.size = screen.get_size()

        self.sub_canvas = []
        self.canvas = []
        self.cap = cap

        self.pencil_size = 10

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils

        
    def run(self, key):
        if key != None:
            self.handleKey(key)

        pos, img = self.handTracking()

        if type(pos) != int:
            self.handleHand(pos)

        self.drawPaint(img)

    def handleKey(self, key):
        if key == 'r':
            self.canvas = []
            self.sub_canvas = []

    def handleHand(self, pos):
        
        if pos[2] < -0.4:
            self.sub_canvas.append((pos[0], pos[1], (0,0,0)))
            print(self.canvas)
        elif len(self.sub_canvas) > 0:
            self.canvas.append((self.sub_canvas))
            self.sub_canvas = []
    def drawPaint(self, img):

        self.drawImage(img, (0,0))
        
        self.drawTransparentRect((255,255,255,200),(self.size[0],self.size[1]), (0,0))

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

    def handTracking(self):
        success, img = self.cap.read()
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.imgRGB = cv2.resize(self.imgRGB, self.size)

        self.imgRGB = cv2.flip(self.imgRGB, 1)

        results = self.hands.process(self.imgRGB)
        pre_dataset = 0

        if results.multi_hand_landmarks:
            finger_tips = 8
            hand_data = results.multi_hand_landmarks[0]

            lm = hand_data.landmark[finger_tips]

            h, w, c = self.imgRGB.shape
            pre_dataset = np.array([lm.x * w, lm.y * h, lm.z])
            self.mpDraw.draw_landmarks(self.imgRGB, hand_data, self.mpHands.HAND_CONNECTIONS)
                
        #cv2.putText(img, f'Direc: {pair_key_direction[str(prediction)]}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        #cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        if key == 27:
            pass
        
        self.imgRGB = cv2.flip(self.imgRGB, 1)

        self.imgRGB = np.rot90(self.imgRGB)
        img = self.pygame.surfarray.make_surface(self.imgRGB)

        return (pre_dataset, img)

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()

    