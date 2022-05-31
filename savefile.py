import os
import load

# Implementasi  pencatatan permainan dalam file
def changecityDataToString(data):
    data[0] = str(data[0])

    for i in range(1, 5):
        data[i] = str(data[i][0]) + ',' + str(data[i][1])

    data[5] = str(data[5])
    data[6] = str(data[6])
    data[7] = str(data[7])

    return data


def save(cityData, playerData, turn, player):
    file = ""
    # Write cityData
    file += "CityData\n"

    for data in cityData:
        data = changecityDataToString(data)
        file += ";".join(data) + "\n"

    file += "PlayerData\n"

    for (keys, val) in playerData.items():
        val = [str(item) for item in val]
        string = keys + ";" + ";".join(val) + "\n"
        file += string 

    file += "Turn\n"

    # Search for player in turn
    n = len(turn)
    for i in range(n):
        if turn[i] == player:
            arr1 = turn[i:n]
            arr2 = turn[:i]
            turn = arr1 + arr2 # membuat player duluan jika dinyalakan savenya

    file += ";".join(turn)

    return file 

def newSaveGame(cityData, playerData, turn, player):
    save_loc = os.getcwd() + "\\save"
    # Asumsi save_loc sudah ada
    os.chdir(save_loc)
    work_dir = os.getcwd()

    # create new
    empty = True
    for dirpath, dirnames, filenames in os.walk(work_dir):
        if len(filenames) > 0:
            existing_save = filenames[len(filenames) - 1].strip(".dat")
            empty = False 

    if not empty:
        savename_length = len(existing_save)
        new_savefile = existing_save[:savename_length - 1] + str(int(existing_save[savename_length - 1]) + 1) + ".dat"

    else:
        new_savefile = "save1.dat"

    print(f"Saving dengan file bernama {new_savefile}")

    # create file 
    f = open(new_savefile, "w")
    saveData = save(cityData, playerData, turn, player)
    f.write(saveData)
    f.close()

    print("Save Berhasil!")


def existingsaveGame(cityData, playerData, turn, player, savefile):
    save_loc = os.getcwd() + "//save"
    # Asumsi save_loc sudah ada
    os.chdir(save_loc)

    # overwrite existing file
    f = open(savefile, "w")
    saveData = save(cityData, playerData, turn, player)
    f.write(saveData)
    f.close()

# implementasi delete pada file  
def removeSaveFile():
    prev_dir = os.getcwd()
    savefile = load.pickSave("hapus")
    if savefile != "":
        print(f"Menghapus savefile {savefile}")
        save_loc = prev_dir + "//save"
        os.chdir(save_loc)
        os.remove(savefile)
        os.chdir(prev_dir)




    


