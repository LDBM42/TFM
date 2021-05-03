import cv2 as cv
from imageai.Detection import ObjectDetection
import numpy as np
import os as os
import time
import urllib.request                                                                   #IPWEBCAM


detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath('yolo.h5')
detector.loadModel(detection_speed="flash") 




cv.startWindowThread()

# open webcam video stream
# cam = cv.VideoCapture(0)
# cam = cv.VideoCapture("rtsp://BRH:ldbm42434445@192.168.2.164/live0")
# URL = "http://192.168.2.213:8080/shot.jpg"                                             #IPWEBCAM
# URL = "http://192.168.2.52:8080/shot.jpg"                                               #IPWEBCAM
URL = "http://192.168.2.122:8080/shot.jpg"                                               #IPWEBCAM

# video size
w, h = 640, 360

# rango completo de visión al rotar
full_w, full_h = w*2, h*2 # 1280x720

# the output will be written to output.avi
# out = cv.VideoWriter(
#     'output.avi',
#     cv.VideoWriter_fourcc(*'MJPG'),
#     2.,
#     (w,h)) #(1920,1080), 640,480

peopleOnly = detector.CustomObjects(person=True)

font = cv.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

center_screen = (int(w/2), int(h/2))

# punto anterior y actual para crear vector
actual_point = center_screen

prev_dx, prev_dy, dx, dy = 90, 90, 90, 90 # centro del cervomotor
centerX, centerY  = (int(w/2), int(h/2))
with open('E:\\DESKTOP\\MASTER INTELIGENCIA ARTIFICIAL\\TFM MAIR Trabajo Fin de Master\\Proyecto Joystick\\JoystickWifi\\security_cam_RL\\coordenadas.txt','w') as f:
                f.write('{"dx":' + str(dx) + ', "dy":' + str(dy) + '}')

angulo_max, angulo_min = (180, 0)
movimiento_en_X = 90
movimiento_en_Y = 90
rango_max_visual, rango_min_visual = (45, -45)

# crear, abrir y escribir archivo de texto --------------------------------------------
# fichero_write = open('output/output.txt', 'w')
# fichero_write.write("ID;Box;Center Point;Move X Y\n")
# fichero_write.flush()
# -------------------------------------------------------------------------------------


while(True):
# while cam.isOpened():
    frame_id += 1
    
    # # Capture frame-by-frame
    # _, frame = cam.read()

    
    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)     #IPWEBCAM
    frame = cv.imdecode(img_arr,-1)                                                      #IPWEBCAM


    # resizing for faster detection
    # frame = cv.resize(frame, (w, h))

    # flip image x-axis
    frame = cv.flip(frame, 1)
    
    detectedImage, detections = detector.detectObjectsFromImage(custom_objects=peopleOnly, output_type="array", 
                                                                input_type='array', input_image=frame, 
                                                                display_percentage_probability=False, 
                                                                display_object_name=False, thread_safe=True)
    
    
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time

    if detections != []:
        box_points = detections[0]['box_points']
        box = [box_points[0], box_points[1], box_points[2]-box_points[0], box_points[3]-box_points[1]]
        x_center = box[0] + (box[2] / 2) 
        y_one_third = box[1] + (box[3] / 2) / 2
        actual_point = (int(x_center), int(y_one_third))
        print(frame_id, end="- ")
        print(box, end=" ")
        print(actual_point, end=" ")

        

        dx = actual_point[0]-center_screen[0]
        dy = actual_point[1]-center_screen[1]
        
        # normalizar la posición a la que se tiene que mover
        dx = round((rango_min_visual - rango_max_visual) * ((dx-(-centerX)) / (centerX-(-centerX))) + rango_max_visual)
        dy = round((rango_min_visual - rango_max_visual) * ((dy-(-centerY)) / (centerY-(-centerY))) + rango_max_visual)


        # print(abs(actual_point[0]-center_screen[0]))
        if (abs(actual_point[0]-center_screen[0])>60):
            movimiento_en_X += dx
            if (movimiento_en_X >= angulo_max): movimiento_en_X = 180
            elif (movimiento_en_X <= angulo_min): movimiento_en_X = 0
            with open('E:\\DESKTOP\\MASTER INTELIGENCIA ARTIFICIAL\\TFM MAIR Trabajo Fin de Master\\Proyecto Joystick\\JoystickWifi\\security_cam_RL\\coordenadas.txt','w') as f:
                f.write('{"dx":' + str(movimiento_en_X) + ', "dy":' + str(prev_dy) + '}')
            prev_dx = movimiento_en_X

        # print(abs(actual_point[1]-center_screen[1]))
        if (abs(actual_point[1]-center_screen[1])>20):
            movimiento_en_Y += dy
            if (movimiento_en_Y >= angulo_max): movimiento_en_Y = 180
            elif (movimiento_en_Y <= angulo_min): movimiento_en_Y = 0
            with open('E:\\DESKTOP\\MASTER INTELIGENCIA ARTIFICIAL\\TFM MAIR Trabajo Fin de Master\\Proyecto Joystick\\JoystickWifi\\security_cam_RL\\coordenadas.txt','w') as f:
                f.write('{"dx":' + str(prev_dx) + ', "dy":' + str(movimiento_en_Y) + '}')
            prev_dy = movimiento_en_Y


        print(movimiento_en_X, movimiento_en_Y)

        # escribir registro en fichero --------------------------------------------------------
        # fichero_write.write(str(frame_id) + ";" + str(box) + ";" + str(actual_point) + 
        #                                     ";" + str(actual_point[0]-center_screen[0]) + "," + 
        #                                     str(center_screen[1]-actual_point[1]) + "\n")
        # fichero_write.flush()
        # -------------------------------------------------------------------------------------

    # Impresion en pantalla ---------------------------------------------------------------------------------------------
    cv.putText(detectedImage, "FPS=" + str(round(fps, 2)), (400, 50), font, 3, (0, 255, 255), 3)
    cv.putText(detectedImage, "x=" + str(movimiento_en_X) + " y=" + str(movimiento_en_Y),
            (10, 50), font, 3, (0, 255, 255), 3)
    cv.arrowedLine(detectedImage, center_screen, actual_point, (0, 0, 0), 3) 
    # --------------------------------------------------------------------------------------------------------------------

    # Write the output video 
    # out.write(detectedImage.astype('uint8'))
    # out.write(frame.astype('uint8'))

    # Display the resulting frame
    cv.imshow('frame',detectedImage)
    # cv.imshow('frame',frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
    # poner en full screem
    # cv.namedWindow("Side Camera", cv.WND_PROP_FULLSCREEN)
    # cv.setWindowProperty("Side Camera",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    # cv.imshow("Side Camera", detectedImage)

# # When everything done, release the capture
# cam.release() 
# # and release the output
# out.release()
# # close file
# fichero_write.close()

# finally, close the window
cv.destroyAllWindows()
cv.waitKey(1)