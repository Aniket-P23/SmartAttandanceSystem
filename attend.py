import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import sys
import time
import pybase64
# starting the webcam using opencv 
cap = cv2.VideoCapture(0)


names=[]

#function for writing the data into text file
fob=open('attendence.txt','a+')
def enterData(z):
    if z in names:
        pass
    else:
        names.append(z)
        z=''.join(str(z))
        fob.write(z+'\n')
    return names

print('Reading...')
#function for check the data is present or not
def checkData(data):
    data=str(data)    
    if data in names:
        print('Already Present')
    else:
        print('\n'+'Roll No: '+str(len(names)+1)+' present done')
        enterData(data)
  
while True:
    _, frame = cap.read() 
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        checkData(obj.data)
        time.sleep(1)
       
    cv2.imshow("Smart Attendance System", frame)

    #closing the program when s is pressed
    if cv2.waitKey(1)& 0xFF == ord('s'):
        cv2.destroyAllWindows()
        break
    
fob.close()
