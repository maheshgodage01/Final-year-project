import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
# from PIL import ImageGrab
 


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('D:\Final Year Project(final)\src\Face_recognition_system\log.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        # for line in myDataList:
        #     entry = line.split(',')
        #     nameList.append(entry[0])
        # if name not in nameList:
        now = datetime.now()
        dtString = now.strftime("%d %B %Y, %I:%M %p")
        f.writelines(f'\n{name},{dtString}')



def verify():
    path = r"D:\Final Year Project(final)\src\Face_recognition_system\known_faces"
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    # print(classNames)
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    count = 100
    while count>0:
        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
    
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),1)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
                cv2.destroyAllWindows()
                return name
            
    
        cv2.imshow('Webcam',img)
        cv2.waitKey(1)
        count-=1
    print("coudnt verify")
    cv2.destroyAllWindows()
    return False

# verify()