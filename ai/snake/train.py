import cv2
import mediapipe as mp
import time
import pandas as pd

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

dataset = {
    "direction": []
}

def append_data(direction, pre_dataset):
    dataset['direction'].append(direction)
    print(pre_dataset)
    for k, v in pre_dataset.items():
        if k not in dataset:
            dataset[k] = []
        
        dataset[k].append(v)

def save_dataset():
    df = pd.DataFrame.from_dict(dataset) 
    df.to_csv('ai/snake/train.csv', index=False)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    pre_dataset = {}
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                pre_dataset[f'{id}x'] = lm.x
                pre_dataset[f'{id}y'] = lm.y

                # if id == 4:
                #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('1'):
        append_data(1, pre_dataset)
    if key == ord('2'):
        append_data(2, pre_dataset)
    if key == ord('3'):
        append_data(3, pre_dataset)
    if key == ord('4'):
        append_data(4, pre_dataset)
    if key == 27:
        print(dataset)
        save_dataset()
        break