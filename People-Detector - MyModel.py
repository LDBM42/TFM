import cv2 as cv
from imageai.Detection import ObjectDetection
import numpy as np
import os as os
import time
import urllib.request                                                                   #IPWEBCAM
import matplotlib.pyplot as plt


from tensorflow.keras.models import load_model
from tensorflow.keras.applications import mobilenet
# import imutils

#Cargar modelo
model = load_model("deepCNN_MOBILENET_TRANSFER_LEARNING_Person_Recognition_OWN_datasets_8_PREPROCESS_FT_03.h5")




# open webcam video stream
URL = "http://192.168.2.52:8080/shot.jpg"                                               #IPWEBCAM

# video size
w, h = 640, 360

font = cv.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

# punto anterior y actual para crear vector
prev_point = (0,0)
actual_point = (0,0)

files_and_directories = os.listdir("training dataset\\output_indoor")
size = len(files_and_directories)
i = 0


while(True):
# while cam.isOpened():
    
    frame_id += 1
    
    if i < size:
        cam = cv.VideoCapture("training dataset\\output_indoor\\" + files_and_directories[i])
        i += 1
    else:
        break
    
    # Capture frame-by-frame
    _, frame = cam.read()


    
    
    
    # img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)     #IPWEBCAM
    # frame = cv.imdecode(img_arr,-1)                                                      #IPWEBCAM
    

    # resizing for faster detection
    frame = cv.resize(frame, (w, h))
    center_screen = (int(w/2), int(h/2))

    # Preprocesar como MobileNet
    frame_preprocess = mobilenet.preprocess_input(frame)

    # agregar una dimension al array para poder predecir dentro del modelo
    frame_preprocess = np.expand_dims(frame_preprocess, axis=0)
    
    # Evaluación del modelo
    bb_pred = model.predict(frame_preprocess)[0]




    # # flip image x-axis
    # frame = cv.flip(frame, 1)

    
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time


    if bb_pred != []:
        prev_point = actual_point

        X, Y, W, H = int(bb_pred[0]*w), int(bb_pred[1]*h), int(bb_pred[2]*w), int(bb_pred[3]*h) 
        pt1, pt2 = (X, Y), (X+W, Y+H)

        # mostrar bounding box
        cv.rectangle(frame, pt1=pt1, pt2=pt2, color=(0,0,255), thickness=2) 

        x_center = X + (W / 2) 
        y_one_third = (Y + (H / 2)) / 2
        actual_point = (int(x_center), int(y_one_third))
        print(frame_id, end="- ")
        print([X, Y, W, H], end=" ")
        print(actual_point, end=" ")
        print("x=" + str(prev_point[0]-center_screen[0]) , "y=" + str(center_screen[1]-prev_point[1]))
        

    # Impresion en pantalla ---------------------------------------------------------------------------------------------
    cv.putText(frame, "FPS=" + str(round(fps, 2)), (400, 50), font, 3, (0, 255, 255), 3)
    # cv.putText(frame, "x=" + str(prev_point[0]-center_screen[0]) + " y=" + str(center_screen[1]-prev_point[1]),
    #            (10, 50), font, 3, (0, 255, 255), 3)
    # cv.arrowedLine(frame, center_screen, actual_point, (0, 0, 0), 3) 
    # --------------------------------------------------------------------------------------------------------------------

    # # Write the output video 
    # # out.write(detectedImage.astype('uint8'))
    # out.write(frame.astype('uint8'))

    # Display the resulting frame
    cv.imshow('frame',frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
    # poner en full screem
    # cv.namedWindow("Side Camera", cv.WND_PROP_FULLSCREEN)
    # cv.setWindowProperty("Side Camera",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    # cv.imshow("Side Camera", detectedImage)

# When everything done, release the capture
cam.release() 

# finally, close the window
cv.destroyAllWindows()
cv.waitKey(1)