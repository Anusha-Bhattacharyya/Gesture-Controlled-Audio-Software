#!/usr/bin/env python3
import tensorflow as tf 
from keras.models import load_model
import cv2
import numpy as np
from random import choice
import json
import os
import h5py

REV_CLASS_MAP = {
    0: "OpenHand",
    1: "ClosedFist",
    2: "ThumbsUp",
    3: "PeaceSignUpwards",
    4: "PeaceSignDownwards",
    5: "PointingLeft",
    6: "Nothing",
}


def mapper(val):
    print(val)
    return REV_CLASS_MAP[val]

model = load_model("finalmodel.h5")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

prev_move = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.rectangle(frame, (8, 25), (315, 335), (0, 255, 0), 2)    
    #cv2.rectangle(frame, (330, 70), (630, 370), (255, 0, 0), 2)

    roi = frame[25:335, 8:315]
    save_path = os.path.join('images', 'current.png')
    print(save_path)
    cv2.imwrite(save_path, roi)

    # extract the region of image within the user rectangle
    #roi = frame[70:300]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (64, 64))

    # predict the move made
    pred = model.predict(np.array([img]))
    gesture_code = np.argmax(pred[0])
    print(gesture_code)
    gesture_name = mapper(gesture_code)
    HAND_LOCATION_X = 1
    HAND_LOCATION_Y = 1
    print(gesture_name)
    with open("gesture.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["gesture_name"] = gesture_name
    data["gesture_started"] = 1
    data["HAND_LOCATION_X"] = HAND_LOCATION_X
    data["HAND_LOCATION_Y"] = HAND_LOCATION_Y

    with open("gesture.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    if prev_move != gesture_name:
        if gesture_name == "Nothing":
            gesture = "Waiting..."
    prev_move = gesture_name

    # display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(frame, "Your Move: " + gesture_name,
                #(10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    #cv2.putText(frame, "Pi's Move: " + computer_move_name,
                #(330, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Gesture: " + gesture_name,
                (100, 450), font, 1, (0, 255, 0), 4, cv2.LINE_AA)

    #if computer_move_name != "nothing":
        #icon = cv2.imread(
            #"test_img/{}.png".format(computer_move_name))
        #icon = cv2.resize(icon, (300, 300))
        #frame[70:370, 330:630] = icon

    cv2.imshow("Gesture-Recognition", frame)

    k = cv2.waitKey(10)
    if k == ord('q'):
        with open("gesture.json", "r") as jsonFile:
            data = json.load(jsonFile)
        data["gesture_started"] = 0
        with open("gesture.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        break

cap.release()
cv2.destroyAllWindows()
