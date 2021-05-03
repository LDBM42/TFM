# leer archivo
file = open("training dataset\\output_outdoor_night\\output_outdoor_night.txt", 'r').readlines()

with open("training dataset\\output_outdoor_night\\output_outdoor_night2.txt", 'w') as f:
    # llenar lista con ID de archivo
    for line in list(file):
        index = line.find(";")
        if line[0:index] == 'ID': 
            f.write(line)
            continue 
        id = int(line[0:index])
        if id < 10:
            line = line.replace(str(id)+";[", "000" + str(id)+";[")
        elif id < 100:
            line = line.replace(str(id)+";[", "00" + str(id)+";[")
        elif id < 1000:
            line = line.replace(str(id)+";[", "0" + str(id)+";[")
        
        f.write(line)



