#  pip install mediapipe
#pip install open-cv
import math
import cv2
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui

mouse= Controller()
video= cv2.VideoCapture(0)

width= int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("what is width: ",width)
print("what is height: ",height)

(screen_width, screen_height) = pyautogui.size()

# draw hands
myhands= mp.solutions.hands

# display landmarks
mydrawing= mp.solutions.drawing_utils

hand_obje= myhands.Hands(min_detection_confidence=0.75,min_tracking_confidence=0.75)

print("what is handObject: ",hand_obje)

pinch=False

def countFingures(img,lst):
    count=0
    global pinch

    thresh=(lst.landmark[0].y*100-lst.landmark[9].y*100)/2
    # print("what is thresh: ",thresh)

    if (lst.landmark[5].y*100 -lst.landmark[8].y*100)>thresh:
        count+=1

    if (lst.landmark[9].y*100 -lst.landmark[12].y*100)>thresh:
        count+=1

    if (lst.landmark[13].y*100 -lst.landmark[16].y*100)>thresh:
        count+=1

    if (lst.landmark[17].y*100 -lst.landmark[20].y*100)>thresh:
        count+=1

    # if(lst.landmark[5].x*100 -lst.landmark[4].x*100)>6: 
    #     count+=1

    totalFinguers=count

    # PINCH


    return totalFinguers



while True:
    dummy,image= video.read()
    flipImage= cv2.flip(image,1)
    # cv2.imshow("hands",image)
    

    result= hand_obje.process(cv2.cvtColor(flipImage,cv2.COLOR_BGR2RGB))
    # print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        hand_keyPoints=result.multi_hand_landmarks[0]

        mydrawing.draw_landmarks(flipImage,hand_keyPoints,myhands.HAND_CONNECTIONS)

        count=countFingures(flipImage,hand_keyPoints)
        cv2.putText(flipImage,"TF: "+str(count),(200,100),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)

        cv2.putText(flipImage,"State: "+str(pinch),(200,150),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)

    cv2.imshow("hands flip",flipImage)

    if cv2.waitKey(25) ==27:
        break

video.release()
cv2.destroyAllWindows()