from .game import Minigame

import cv2
import numpy as np
import mediapipe as mp

import pickle

from random import randint

class Snake(Minigame):
    def __init__(self, pygame, screen, clock, cap, switch_game):
        super().__init__(pygame, screen, clock)
        self.direction_past = None
        self.direction = None
        self.size = screen.get_size()
        self.switch_game = switch_game

        self.snake_size = self.size[1] / 13
        self.snake_body = np.array([[*self.newRandomScreenPos(), self.snake_size]])
        self.snake_length = 1
        
        self.fruit_pos = self.newRandomScreenPos()
        self.fruit_size = self.snake_size*0.60

        pickle_in = open('ai/snake/model.pickle', "rb")
        self.model = pickle.load(pickle_in)

        self.cap = cap
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1)
        self.mpDraw = mp.solutions.drawing_utils

    def run(self, key, mouse):
        if key != None:
            self.handleKey(key)

        """
        prediction, img =self.handTracking()

        if prediction != 0:
            self.handleHand(prediction)"""

        self.move()
        self.renderScreen(img=False)
        self.handleEatFruit()
        self.handleEatItSelf()

        surface = self.pygame.display.get_surface()#surfarray.array3d(self.screen)
        surface = self.apply_blooming(surface)
        #img = self.pygame.surfarray.make_surface(surface)
        self.screen.blit(surface, (0,0))

        self.renderScreen(img=False)



    def handleKey(self, key):
        pair_key_direction = {
            "d": "right",
            "a": "left",
            'w': "up",
            "s": "down"
        }
        if key in pair_key_direction.keys():
            self.direction_past = self.direction
            self.direction = pair_key_direction[key] 
            if self.direction == None or self.is_oposite_direction():
                 self.direction = self.direction_past
    def handleHand(self, direction):
        pair_key_direction = {
            "1": "up",
            "2": "down",
            '3': "left",
            "4": "right"
        }

        str_direction = str(direction)
        self.direction_past = self.direction

        self.direction = pair_key_direction[str_direction] 
        if self.direction == None or self.is_oposite_direction() == True:
            self.direction = self.direction_past

    def is_oposite_direction(self):
        directions_oposite = {
            "up": "down",
            "down": "up",
            'left': "right",
            "right": "left"
        }

        return self.direction_past == directions_oposite[self.direction]
        

    def move(self):
        if self.direction != None:
            if self.direction == "left":
                self.snake_body = np.append(self.snake_body, np.array([[self.snake_body[-1][0] - self.snake_size/3, self.snake_body[-1][1], self.snake_size]]), axis=0)
            
            if self.direction == "right":
                self.snake_body = np.append(self.snake_body, np.array([[self.snake_body[-1][0] + self.snake_size /3, self.snake_body[-1][1], self.snake_size]]), axis=0)

            if self.direction == "up":
                self.snake_body = np.append(self.snake_body, np.array([[self.snake_body[-1][0], self.snake_body[-1][1] - self.snake_size /3, self.snake_size]]), axis=0)

            if self.direction == "down":
                self.snake_body = np.append(self.snake_body, np.array([[self.snake_body[-1][0], self.snake_body[-1][1] + self.snake_size /3, self.snake_size]]), axis=0)

        if self.snake_body[-1][1] >= self.size[1]:
            self.snake_body[-1][1] = 0

        if self.snake_body[-1][0] >= self.size[0]:
            self.snake_body[-1][0] = 0

        if self.snake_body[-1][1] < 0:
            self.snake_body[-1][1] = self.size[1]

        if self.snake_body[-1][0] < 0:
            self.snake_body[-1][0] = self.size[0]

        if len(self.snake_body) > self.snake_length:
            self.snake_body = np.delete(self.snake_body, 0, axis=0)
    
    def handleEatItSelf(self):
        for part in self.snake_body[1:]:
            if part[0] == self.snake_body[0][0] and part[1] == self.snake_body[0][1]:
                self.switch_game("interface")

    def handleEatFruit(self):
        difference_pos_x = self.snake_body[-1][0] - self.fruit_pos[0]
        difference_pos_y = self.snake_body[-1][1] - self.fruit_pos[1]

        tolerance = self.snake_size
        
        if ( difference_pos_x < tolerance and difference_pos_x > -tolerance ) and ( difference_pos_y < tolerance and difference_pos_y > -tolerance ):

            self.fruit_pos = self.newRandomScreenPos()
            self.snake_length += 1
            self.snake_body[-1, 2] = self.snake_body[-1, 2] * 1.15

    def newRandomScreenPos(self):
        return (randint(0, self.size[0]-round(self.snake_size/2)), randint(0, self.size[1]-round(self.snake_size)/2))

    def renderScreen(self, img):
        if img != False:
            self.drawImage(img, (0,0))
        #(130,184,139,100)
        self.drawTransparentRect((0,0,0,255),(self.size[0],self.size[1]), (0,0))

        self.draw((200, 0,0), (self.fruit_pos[0], self.fruit_pos[1], self.fruit_size, self.fruit_size))
        #(41,57,47)
        for part in self.snake_body:
            self.draw((255,255,255), (part[0]-part[2]/2, part[1]-part[2]/2, part[2], part[2]))

    def handTracking(self):
        success, img = self.cap.read()
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(self.imgRGB)
        prediction = 0
        pre_dataset = np.array([])
        if results.multi_hand_landmarks:
            finger_tips = [4,8,12,16,20]
            hand_data = results.multi_hand_landmarks[0]

            for i in range(5):
                lm = hand_data.landmark[finger_tips[i]-1]
                pre_dataset = np.append(pre_dataset, [lm.x, lm.y])
            self.mpDraw.draw_landmarks(self.imgRGB, hand_data, self.mpHands.HAND_CONNECTIONS)
                
        if results.multi_hand_landmarks:
            prediction = self.model.predict([pre_dataset[:10]])[0]
        pair_key_direction = {
            "1": "up",
            "2": "down",
            '3': "left",
            "4": "right"
        }
        img = cv2.flip(img, 1)
        #cv2.putText(img, f'Direc: {pair_key_direction[str(prediction)]}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        #cv2.imshow("Image", img)
        key = cv2.waitKey(1)

        if key == 27:
            pass
        img = cv2.resize(self.imgRGB, self.size)
        img = np.rot90(img)
        img = self.pygame.surfarray.make_surface(img)

        return (prediction, img)

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()