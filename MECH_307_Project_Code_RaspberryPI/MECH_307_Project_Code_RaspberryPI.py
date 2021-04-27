
import cv2
import serial

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #set the face cascade file to a variable
xPos = 0 #initialize x position variable
yPos = 0 #Initialize y position variable
fire = 0 #set fire state to 0
width = 500 #desired video width in pixels
height = 1080 #desired video height in pixels
cap = cv2.VideoCapture(0) #initalize video capture
cap.set(3,width) #set video width (pixels)
cap.set(4,height) # set video height (pixels)
width = cap.get(3) #re-sets variable for video width to actual video width (in pixels)
height = cap.get(4) #re-sets variable for video height to actual video height (in pixels)

#boxTargetSize = 100 #number of square pixels for target box
boxPercent = 0.03 #Percent of the screen the targeting box takes up (Decimal form)
boxTargetSize = pow(boxPercent * width * height,1 / 2) #Calculates number of square pixels for target box
boxTargetPts1 = (int(width / 2 - boxTargetSize / 2),int(height / 2 - boxTargetSize / 2)) #Calculate first point for target box
boxTargetPts2 = (int(width / 2 + boxTargetSize / 2),int(height / 2 + boxTargetSize / 2)) #Calculate second point for target box
#boxTargetCenter = 0
stroke = 2 #Sets stroke size for shapes
frameDelay = 10 # Sets the delay in ms between each frame.  1 is minimum

while(True): #wait for serial connection
    try:
        ser = serial.Serial('COM3',19200) # Serial communication initialization For Windows
        #ser = serial.Serial('/dev/ttyACM0',19200) # Serial communication initialization For Linux
        print("serial connection successful")
        break
    except:
        print("connecting...")
        pass #do nothing
    #start facial recognition
while(True):
    ret, frame = cap.read()
    #frame = cv2.flip(frame,0) #Flip frame upside down for Raspberry Pi Camera
    frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(frameGray,1.2,4)
    #for (x,y,w,h) in faces:
        #cv2.rectangle(frame,(x,y),(x + w,y + h),(255,0,0),stroke) #Draw rectangle around a face
        #cv2.circle(frame,(int(x + w / 2),int(y + h / 2)),5,(255,0,0),stroke) #draw a circle at the center of a face
    try:
        #if faces[0,0] + (faces[0,2] / 2) > boxTargetPts1[0] and faces[0,1] + (faces[0,3] / 2) > boxTargetPts1[1] and faces[0,0] + (faces[0,2] / 2) < boxTargetPts2[0] and faces[0,1] + (faces[0,3] / 2) < boxTargetPts2[1]:
        #if faces[0,0] + (faces[0,2] / 2) > boxTargetPts1[0] and faces[0,0] + (faces[0,2] / 2) < boxTargetPts2[0]:    
            #cv2.rectangle(frame,boxTargetPts1,boxTargetPts2,(0,255,0),stroke) #Draw green rectangle if face is within target area
        #    fire = fire + 5
        #    if fire > 100:
        #        fire = 0
        #else:
            #cv2.rectangle(frame,boxTargetPts1,boxTargetPts2,(255,0,0),stroke)
            ##draw a blue rectangle around target area
        #    fire = 0
        xPos = int(50 - 100 * (faces[0,0] + (faces[0,2] / 2)) / width) #Maps the x-center of face0 in the camera view from -50 to 50
        yPos = int(100 - 100 * (faces[0,1] + (faces[0,3] / 2)) / height) #Maps the y-center of face0 in the camera view from 0 to 100
        if abs(xPos)<15:
            fire=fire+10
        else:
            fire = 0
        posData = str(xPos) + " " + str(yPos)+" "+str(fire) #Convert x and y position data into a string with a 'space' separator
        print(posData) #Display the position to be sent to arduino
        ser.write(str(posData).encode('ascii')) #sends a serial string to the arduinioP
    except:
        #print("No Face Found")
        #cv2.rectangle(frame,boxTargetPts1,boxTargetPts2,(0,0,255),stroke)
        ##draw a red rectangle around target area
        pass

    #cv2.imshow("frame", frame) #display video
    if cv2.waitKey(frameDelay) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()