import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd
import cv2 as cv



try:
    from PIL import Image
except ImportError:
    import Image


index = 0



def LeerArchivo_y_AlmacenarDatos(index):
    # leer archivo
    file = pd.read_table("training dataset\\output_indoor\\output_indoor.txt", sep=";")
    id = file.iloc[index, 0]
    if id < 10:
        imnum = "000" + str(id)
    elif id < 100:
        imnum = "00" + str(id)
    elif id < 1000:
        imnum = "0" + str(id)

    bb = eval(file.iloc[index, 1]) # coordenadas del boundingbox
    # bb = eval(list(file[file['ID'] == int(imnum)]['Box'])[0]) # Buscar por número
    bb_points = [bb[0], bb[1], bb[0]+bb[2], bb[1]+bb[3]]    # x1, y1, x2, y2

    # Open image file
    original_image = np.array(Image.open("training dataset\\output_indoor\\" + imnum + "-output.jpg"))

    # Cantidad de archivos
    max_index = len(file)-1

    # Registro
    reg = file.iloc[index]
    str_reg = str(reg[0]) + ';' + str(reg[1]) + ';' + str(reg[2]) + ';' + str(reg[3]) + '\n'

    return imnum, bb, bb_points, original_image, max_index, str_reg


# almacenar datos
imnum, bb, bb_points, original_image, max_index, str_reg = LeerArchivo_y_AlmacenarDatos(index)



# Coordenadas de la imagen
ancho = original_image.shape[1]
alto = original_image.shape[0]
intervalo = 20

# Obtener la cantidad de cuadrados en el grid
nx=ancho/intervalo
ny=alto/intervalo

# para mover centro de camara
izq_der = 0
ar_ab = 0


# crear, abrir y escribir archivo de texto --------------------------------------------
fichero_write = open("training dataset\\output_indoor\\output_indoor2.txt", 'w')
fichero_write.write("ID;Box;Center Point;Move X Y\n")
fichero_write.flush()
# -------------------------------------------------------------------------------------

while(True):
    
    image = original_image.copy() # Realizar una copia para no cambiar el original y poder actualizar la imagen
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB) # Convertir de BGR a RGB

    # bounding box
    # boundingbox = plt.Rectangle((bb[0],bb[1]), bb[2], bb[3], fc='red')
    cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)

    # agregar rectangulo
    left = ((nx/2)*intervalo)+(intervalo*4)-izq_der
    right = intervalo*2
    top = ((ny/2)*intervalo)-intervalo-ar_ab
    bottom = intervalo*2
    agent_points = [int(left), int(top), int(left+right), int(top+bottom)]     # x1, y1, x2, y2
    
    # plt.gca().add_patch(boundingbox)
    # rectangle = plt.Rectangle((left,top), bottom, right, fc='blue')
    cv.putText(image, imnum, (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
    cv.rectangle(image,(agent_points[0],agent_points[1]),(agent_points[2],agent_points[3]),(255,0,0),1)
    # plt.gca().add_patch(rectangle)

    # plt.xticks(np.arange(0, ancho, intervalo))
    # plt.yticks(np.arange(0, alto, intervalo))
    # plt.grid(linestyle='-', linewidth=.5)
    # plt.imshow(image)
    cv.imshow('frame',image)
    # plt.show()

    # calcular si el agente toca algún pedazo del bounding box
    # if not (bb_points[0] < agent_points[2] and bb_points[2] > agent_points[0] and 
    # bb_points[1] < agent_points[3] and bb_points[3] > agent_points[1]):
    #     fichero_write.write(str_reg)
    #     fichero_write.flush()
    #     if index <= max_index:
    #         index = index+1
    #         imnum, bb, bb_points, original_image, max_index, str_reg = LeerArchivo_y_AlmacenarDatos(index) # almacenar datos
    #     else: break
        #print("superpuestos")


    k = cv.waitKey(33)
    if k==ord('q'): break
    elif k==ord('a'): 
        izq_der = izq_der+intervalo
    elif k==ord('d'): 
        izq_der = izq_der-intervalo
    elif k==ord('w'):
        ar_ab = ar_ab+intervalo
    elif k==ord('s'):
        ar_ab = ar_ab-intervalo
    elif k==ord('z'):
        if index <= max_index:
            index = index+1
            imnum, bb, bb_points, original_image, max_index, str_reg = LeerArchivo_y_AlmacenarDatos(index) # almacenar datos
    elif k==ord('1'):
        bb_points[0] = bb_points[0]-1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('2'):
        bb_points[0] = bb_points[0]+1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('4'):
        bb_points[2] = bb_points[2]-1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('5'):
        bb_points[2] = bb_points[2]+1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('*'):
        bb_points[1] = bb_points[1]-1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('9'): 
        bb_points[1] = bb_points[1]+1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('6'):
        bb_points[3] = bb_points[3]-1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('3'):
        bb_points[3] = bb_points[3]+1
        cv.rectangle(image,(bb_points[0],bb_points[1]),(bb_points[2], bb_points[3]),(0,255,0),1)
    elif k==ord('g'):
        nueva_coord = "[" + str(bb_points[0]) + ", " + str(bb_points[1]) + ", " + str(bb_points[2]-bb_points[0]) + ", " + str(bb_points[3]-bb_points[1]) + "]"
        print(str_reg)
        str_reg = str_reg.replace(str(bb),  nueva_coord)
        print(str_reg)

        # escribir nuevas coordenadas en fichero
        fichero_write.write(str_reg)
        fichero_write.flush()

        if index <= max_index:
            index = index+1
            imnum, bb, bb_points, original_image, max_index, str_reg = LeerArchivo_y_AlmacenarDatos(index) # almacenar datos

# Save the figure
# fig.savefig('0431-output_GRID.jpg',dpi=my_dpi)



