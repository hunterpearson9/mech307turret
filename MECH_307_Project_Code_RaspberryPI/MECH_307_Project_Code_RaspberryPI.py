import cv2 #Import OpenCV Library
import serial #Import serial communication

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

frameDelay = 1 # Sets the delay in ms between each frame.  1 is minimum

while(True): #wait for serial connection
    try:
        #ser = serial.Serial('COM3',19200) # Serial communication initialization For Windows
        ser = serial.Serial('/dev/ttyACM0',19200) # Serial communication initialization For Linux
        print("serial connection successful")
        break
    except:
        #print("connecting...")
        pass #do nothing

#start facial recognition
while(True):
    ret, frame = cap.read() #Read image from camera; store to 'frame'
    frame = cv2.flip(frame,0) #Flip image upside down for Raspberry Pi Camera
    frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Converts image to grayscale for improved facial recognition
    faces = faceCascade.detectMultiScale(frameGray,1.2,4) #Detect faces in image
    try:
        xPos = -1*int(50 - 100 * (faces[0,0] + (faces[0,2] / 2)) / width) #Maps the x-center of face0 in the camera view from -50 to 50
        yPos = int(100 - 100 * (faces[0,1] + (faces[0,3] / 2)) / height) #Maps the y-center of face0 in the camera view from 0 to 100
        if abs(xPos)<5 and fire <100: #Check if face is centered in the image
            fire=fire+12 #Add 12 to the "fire" state. Dart gun will fire at or above 100
        else: 
            fire = 0 #If a face is not centered in the image, reset "fire" state to 0
        posData = str(xPos) + " " + str(yPos)+" "+str(fire) #Convert x and y position data into a string with a 'space' separator
        #print(posData) #Display the position data to be sent to arduino
        ser.write(str(posData).encode('ascii')) #sends a serial string to the arduinioP
    except:
        pass #do nothing
    
    #cv2.imshow("frame", frame) #display video
    if cv2.waitKey(frameDelay) & 0xff == ord("q"): #Waits for the 'q' key to be pressed and delays for 1ms
        break
cap.release() #Stop video capture
cv2.destroyAllWindows()