from numpy.core.fromnumeric import shape
from .game import Minigame

import cv2
import mediapipe as mp
import numpy as np

from random import randint

class Obstacles(Minigame):
    def __init__(self, pygame, screen, clock, cap):
        super().__init__(pygame, screen, clock)
        self.direction_past = None
        self.direction = None
        self.size = screen.get_size()
        print(self.size)

        self.finger_pos = (0,0)
        self.finger_pos_size = 30

        self.obstacles = []
        self.max_obstacles = 1
        self.obstacles_speed = 14

        self.score = 0

        self.cap = cap
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils

        
    def run(self, key, mouse):
        if key != None:
            self.handleKey(key)

        finger_pos, img =self.handTracking()

        if finger_pos != 0:
            self.handleHand(finger_pos)

        if mouse != None:
            self.handleMouse(mouse)
        self.moveObstacle()
        self.renderScreen(img)

    def handleKey(self, key):
        pass

    def handleMouse(self, mouse):
        self.finger_pos = (mouse[0], mouse[1])

    def handleHand(self, finger_pos):
        self.finger_pos = finger_pos

    def moveObstacle(self):
        if len(self.obstacles) == 0:
            rand_size = randint(self.finger_pos_size, round(self.size[0]/4.3))
            randx = randint(rand_size, self.size[0] - rand_size)
            self.obstacles.append([rand_size, randx, -rand_size])
        else:
            for obstacle in self.obstacles:
                obstacle[2] += ((self.size[0] - obstacle[0])**2) / (self.obstacles_speed**4)
        
        if len(self.obstacles) >= 1:
            oldObstacles = self.obstacles
            self.obstacles = list(filter(lambda l: l[2] < self.size[1], self.obstacles))

            if self.obstacles < oldObstacles:
                if self.obstacles_speed > 8:
                    self.obstacles_speed -= 0.2
                if self.finger_pos_size < 45:
                    self.finger_pos_size += 1

                self.score += 1

            for obstacle in self.obstacles:
                finger_touch_x_side = (self.finger_pos[0] >= obstacle[1] and self.finger_pos[0] <= obstacle[1] + obstacle[0])

                finger_touch_y_side = (self.finger_pos[1] >= obstacle[2] and self.finger_pos[1] <= obstacle[2] + obstacle[0])

                if finger_touch_x_side and finger_touch_y_side:
                    self.restart()
    def restart(self):
        self.finger_pos = (0,0)
        self.finger_pos_size = 30

        self.obstacles = []
        self.obstacles_speed = 12
        self.max_obstacles = 1

        self.score = 0

    def renderScreen(self, img):

        self.drawImage(img, (0,0))
        
        self.drawTransparentRect((255,255,255,50),(self.size[0],self.size[1]), (0,0))

        for obstacle in self.obstacles:
            self.draw((200,0,0), (obstacle[1], obstacle[2], obstacle[0], obstacle[0]))

        self.draw((0, 0,0), (self.finger_pos[0] - self.finger_pos_size/2, self.finger_pos[1] - self.finger_pos_size/2, self.finger_pos_size, self.finger_pos_size ))

    def handTracking(self):
        success, img = self.cap.read()
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.imgRGB = cv2.resize(self.imgRGB, self.size)

        self.imgRGB = cv2.flip(self.imgRGB, 1)

        results = self.hands.process(self.imgRGB)
        finger_pos = 0
        if results.multi_hand_landmarks:
            finger_tips = 8
            hand_data = results.multi_hand_landmarks[0]
            h, w, c = self.imgRGB.shape
            lm = hand_data.landmark[finger_tips-1]
            finger_pos = (lm.x*w, lm.y*h)
            self.mpDraw.draw_landmarks(self.imgRGB, hand_data, self.mpHands.HAND_CONNECTIONS)
                
        cv2.putText(self.imgRGB, f'Score: {str(self.score)}', (10, self.size[1]-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 3)

        #cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        if key == 27:
            pass
        
        self.imgRGB = cv2.flip(self.imgRGB, 1)

        img = np.rot90(self.imgRGB)
        img = self.pygame.surfarray.make_surface(img)

        return (finger_pos, img)

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()