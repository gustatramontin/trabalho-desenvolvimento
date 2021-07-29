import cv2
import mediapipe as mp
import time
import pandas as pd
import numpy as np

import pickle


pickle_in = open('ai/snake/model.pickle', "rb")
model = pickle.load(pickle_in)

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    pre_dataset = np.array([])
    if results.multi_hand_landmarks:
        finger_tips = [4,8,12,16,20]
        hand_data = results.multi_hand_landmarks[0]

        for i in range(5):
            lm = hand_data.landmark[finger_tips[i]-1]
            pre_dataset = np.append(pre_dataset, [lm.x, lm.y])
        mpDraw.draw_landmarks(img, hand_data, mpHands.HAND_CONNECTIONS)
        """
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                #h, w, c = img.shape
                #cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                if id in [4,8,12,16,20]:
                    pre_dataset = np.append(pre_dataset, [lm.x, lm.y])

                # if id == 4:
                #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        """
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    prediction = "?"
    #print(pre_dataset)
    if results.multi_hand_landmarks:
        try:
            prediction = model.predict([pre_dataset[:10]])[0]
        except:
            print('Two Hands')
    img = cv2.flip(img, 1)
    cv2.putText(img, f'FPS: {str(int(fps))} & Direc: {prediction}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == 27:
        break