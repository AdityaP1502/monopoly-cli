import os
def findAvailableSave():
    prev_dir = os.getcwd()
    os.chdir("save")
    work_dir = os.getcwd()
    os.chdir(prev_dir)
    for dirpath,dirnames,filenames in os.walk(work_dir):
        return filenames

def pickSave(format):
    saveNames = findAvailableSave()
    i = 0
    if len(saveNames) > 0:
        for saveName in saveNames:
            print(str(i+1) + ". " + saveName.split(".dat")[0])
            i += 1

        userChoice = int(input(f"Pilih save yang ingin di{format}\n>"))
        while userChoice > i + 1:
            print("Harap memasukkan pilihan yang benar.")
            userChoice = int(input(f"Pilih save yang ingin di{format}\n>"))

        saveChoice = saveNames[userChoice - 1]

        return saveChoice

    print("Tidak Ada save yang tersedia!")

    return ""

def loadSave(savefile):
    data_matriks = []
    prev_dir = os.getcwd()
    os.chdir("save")
    f = open(savefile, "r")
    raw_lines = f.readlines()
    f.close()
    os.chdir(prev_dir)

    lines = [raw_line.replace("\n", "") for raw_line in raw_lines]

    del lines[0]
    count = 0

    while len(lines) > 0:
        data_arr = []
        line = lines[0]

        if line == "PlayerData":
            del lines[count]
            break 

        else:
            arr = line.split(";")
            data_arr.append(arr[0].strip())

            for i in range(1, 5):
                data = (arr[i].strip()).split(",")
                data = [int(item) for item in data]
                data_arr.append(data)

            data_arr.append(int(arr[5]))
            data_arr.append(int(arr[6])) #LVL of the city
            data_arr.append(arr[7]) #Ownership
            
            data_matriks.append(data_arr)
            del lines[count]

    dict = {}
    while len(lines) > 0:
        line = lines[0]

        if line == "Turn":
            del lines[count]
            break 

        else:
            arr = line.split(";")
            keys = arr[0]
            val = arr[1:]
            val = [int(item) for item in val]
            dict[keys] = val

            del lines[count]

    for line in lines:
        turn = line.split(";")

    return data_matriks, dict, turn 

def findAvailableMap():
    prev_dir = os.getcwd()
    os.chdir("map")
    work_dir = os.getcwd()

    os.chdir(prev_dir)
    for dirpath,dirnames,filenames in os.walk(work_dir):
        return filenames

def pickMap():
    mapNames = findAvailableMap()
    i = 0
    for mapName in mapNames:
        print(str(i+1) + ". " + mapName.split(".csv")[0])
        i += 1

    userChoice = int(input("Pilih Map yang ingin dimainkan\n>"))
    while userChoice > i + 1:
        print("Harap memasukkan pilihan yang benar.")
        userChoice = int(input("Pilih Map yang ingin dimainkan\n>"))

    mapChoice = mapNames[userChoice - 1]

    return mapChoice

def loadMap(mapname):
    prev_dir = os.getcwd()
    os.chdir("map")

    f = open(mapname, "r")
    os.chdir(prev_dir)
    raw_lines = f.readlines()
    f.close()
    lines = [raw_line.replace("\n", "") for raw_line in raw_lines]

    cityData = convertFileToData(lines)

    return cityData

def convertFileToData(lines):
    # Implementasi kelompok 3
    # List lokasi dijadikan list of list, yang tiap list isinya data - data lokasi tersebut seperti nama, harga, level, dan owner
    data_matriks = []
    delimiter = ";"

    del lines[0]

    for line in lines:
        data_arr = []
        arr = line.split(delimiter)

        data_arr.append(arr[0].strip())
        for i in range(1, len(arr) - 1):
            data_arr.append([int(arr[i].strip())] * 2)

        data_arr.append(int(arr[len(arr) - 1].strip()))
        data_arr.append(0) #LVL of the city
        data_arr.append("") #Ownership
            
        data_matriks.append(data_arr)
        
    return data_matriks
    

