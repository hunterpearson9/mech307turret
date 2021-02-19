
import cv2
import serial

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #set the face cascade file to a variable
ser = serial.Serial('COM3',9600)
pos = 0

width = 500 #desired video width in pixels
height = 1080 #desired video height in pixels
cap = cv2.VideoCapture(0)
cap.set(3,width) #video width
cap.set(4,height) #video height
width = cap.get(3) #re-sets variable for video width to actual video width (in pixels)
height = cap.get(4) #re-sets variable for video height to actual video height (in pixels)

#boxTargetSize = 100 #number of square pixels for target box
boxPercent = 0.03 #Percent of the screen the targeting box takes up (Decimal form)
boxTargetSize = pow(boxPercent * width * height,1 / 2) #Calculates number of square pixels for target box
boxTargetPts1 = (int(width / 2 - boxTargetSize / 2),int(height / 2 - boxTargetSize / 2))
boxTargetPts2 = (int(width / 2 + boxTargetSize / 2),int(height / 2 + boxTargetSize / 2))
boxTargetCenter = 0

stroke = 2 #Sets stroke size for shapes
while(True):
    ret, frame = cap.read()
    frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(frameGray,1.2,4)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x + w,y + h),(255,0,0),stroke) #Draw rectangle around face
        cv2.circle(frame,(int(x + w / 2),int(y + h / 2)),5,(255,0,0),stroke)

    try:
        if faces[0,0] + (faces[0,2] / 2) > boxTargetPts1[0] and faces[0,1] + (faces[0,3] / 2) > boxTargetPts1[1] and faces[0,0] + (faces[0,2] / 2) < boxTargetPts2[0] and faces[0,1] + (faces[0,3] / 2) < boxTargetPts2[1]:
                cv2.rectangle(frame,boxTargetPts1,boxTargetPts2,(0,255,0),stroke)
        else:
            cv2.rectangle(frame,boxTargetPts1,boxTargetPts2,(255,0,0),stroke)
        pos = int(180 - 180 * (faces[0,0] + (faces[0,2] / 2)) / width) #Maps the center of face0 in the camera view to 180 degrees
        #print(pos) #Display the position to be sent to arduino
        ser.write(str(pos).encode('ascii')) #sends a serial string to the arduinio
    except:
        #print("No Face Found")
        cv2.rectangle(frame,boxTargetPts1,boxTargetPts2,(0,0,255),stroke)

    cv2.imshow("frame", frame)
    if cv2.waitKey(15) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()