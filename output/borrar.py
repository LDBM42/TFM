from os import remove

# leer archivo
file = open("output.txt", 'r').readlines()

no_borrar = []

# llenar lista con ID de archivo
for line in list(file):
    index = line.find(";")
    if line[0:index] == 'ID': continue # no almacenar encabezado
    no_borrar.append(int(line[0:index]))

# # borrar solo los datos no encontrados
for id in range(1, max(no_borrar)+1):
    if id not in no_borrar:
        if id < 10:
            remove("000" + str(id) + "-output.jpg")
        elif id < 100:
            remove("00" + str(id) + "-output.jpg")
        elif id < 1000:
            remove("0" + str(id) + "-output.jpg")
        elif id >= 1000:
            remove(str(id) + "-output.jpg")
