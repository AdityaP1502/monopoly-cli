import display as dp
import game as gm
import load as ld
import savefile as save

def startNewGame():
     # LOAD MAP IF START NEW GAME
    mapChoice = ld.pickMap()
    cityData = ld.loadMap(mapChoice)
    total_block = len(cityData) # Total block is a multiple of 4 

    k_x = total_block // 4 + 1 # Total block in x direction
    k_y = k_x - 2 # Total block in between top and bottom

    playerData, turn = gm.createPlayer()
    player_count = len(playerData)

    return k_x, k_y, cityData, playerData, player_count, turn

def loadSaveFile():
    savefile = ld.pickSave("mainkan")
    if savefile != "":
        cityData, playerData, turn = ld.loadSave(savefile)

        total_block = len(cityData) # Total block is a multiple of 4 

        k_x = total_block // 4 + 1 # Total block in x direction
        k_y = k_x - 2 # Total block in between top and bottom

        player_count = len(playerData)

    else:
        print("Memulai game baru.")
        k_x, k_y, cityData, playerData, player_count, turn = startNewGame()
    
    return k_x, k_y, cityData, playerData, player_count, turn

def viewData(player, playerData, cityData):
    # Kelompok 5
    print("Data Player")
    print(f"Username : {player}")
    print(f"Jumlah uang : {playerData[player][1]}")
    curr_pos = playerData[player][2]
    print(f"Lokasi sekarang : {cityData[curr_pos][0]}")
    print("Berikut properti yang Anda miliki:")
    count = 0

    for i in range(len(cityData)):
        data = cityData[i]

        if data[7] == player:
            count += 1
            print(f"{count}. Kota di {data[0]}")
            print(f"Harga sewa {data[1][1]}")
            print(f"Harga jual {data[4][1]}")

    if count == 0:
        print("Anda masih belum mempunyai properti.")

if __name__ == "__main__":
    # START

    # DISPLAY PROPERTIES
    n_x = 32
    n_y = 4

    print("Pilih operasi yang Anda ingin lakukan (Pilih nomor saja)!\n1.START NEW GAME\n2.LOAD\n3.Hapus")
    choice = input(">")

    while (ord(choice) > 51 or ord(choice) < 49):
        print("Masukkan Anda salah. Harap memilih NOMORNYA saja yaitu antara 1 - 3.")
        print("Pilih operasi yang Anda ingin lakukan (Pilih nomor saja)!\n1.START NEW GAME\n2.LOAD")
        choice = input(">")

    if choice == "1":
        newGame = True 
        k_x, k_y, cityData, playerData, player_count, turn = startNewGame()
    
    elif choice == "2":
        newGame = False
        k_x, k_y, cityData, playerData, player_count, turn = loadSaveFile()

    else:
        save.removeSaveFile()
        print("Pilih operasi yang Anda ingin lakukan (Pilih nomor saja)!\n1.START NEW GAME\n2.LOAD")
        choice = input(">")

        while (ord(choice) > 50 or ord(choice) < 49):
            print("Masukkan Anda salah. Harap memilih NOMORNYA saja yaitu antara 1 - 2.")
            print("Pilih operasi yang Anda ingin lakukan (Pilih nomor saja)!\n1.START NEW GAME\n2.LOAD")
            choice = input(">")

        if choice == "1":
            newGame = True 
            k_x, k_y, cityData, playerData, player_count, turn = startNewGame()
    
        elif choice == "2":
            newGame = False
            k_x, k_y, cityData, playerData, player_count, turn = loadSaveFile()

    is_bankrupt = False # Flag if someone has lost the game 

    # Create variabel to display game
    TransformMap = dp.mapping(k_x, k_y)
    arrOfText = dp.createArrOfText(cityData, TransformMap)

    # DISPLAY SCREEN
    screen = dp.Screen(n_x, k_x, n_y, k_y, arrOfText) 
    startData = dp.startArr(k_x, k_y, n_x, n_y)


    print("Please Wait!")

    for i in range(1000):
        print()

    print("Selamat Bermain!")
    dp.Display(screen)

    while player_count != 1:
        for player in turn:
            print(f"Sekarang giliran : {player}")
            Y = input("MAU ROLL?")

            if Y == "Y" or Y == "y":
                curr_pos = gm.movePlayer(playerData, player, 8, n_x, startData, screen, TransformMap)
                print(f"Anda Mendarat di {cityData[curr_pos][0]}")

                if not gm.checkCity(curr_pos, cityData):
                    gm.buy(curr_pos, cityData, playerData, player, startData, TransformMap, screen, n_x)

                else:
                    is_bankrupt = gm.pay(curr_pos, cityData, player, playerData, TransformMap, screen, n_x, startData)
                    if is_bankrupt == False:
                        gm.upgrade(curr_pos, cityData, player, playerData)

                if is_bankrupt:
                    player_count -= 1
                    turn.remove(player)
                    is_bankrupt = False
                

            elif Y == "N" or Y == "n":
                print("List Command yang dapat dilakukan:\n1.save\n2.exit\n3.view\n4.lanjut")
                choice = input("Command apa yang ingin Anda jalankan?\n>")

                if choice == "exit":
                    player_count = 1
                    break

                elif choice == "save":
                    if newGame:
                        save.newSaveGame(cityData, playerData, turn, player)

                    else:
                        save.existingsaveGame(cityData, playerData, turn, player)
                    
                    player_count = 1
                    break

                elif choice == "view":
                   viewData(player, playerData, cityData)

    pemenang = list(playerData.keys()).pop()
    print(f"Pemenangnya adalah {pemenang}")

                    

         



