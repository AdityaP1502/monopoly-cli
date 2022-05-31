from random import randint, shuffle
from display import Display, displayRoll, modifyScreen, padding

def createTurn(arrUsername):
    shuffle(arrUsername)
    return arrUsername

def createPlayer():
    dict = {}
    base_money = 50000
    curr_pos = 0
    choice = int(input("Pilihlah jumlah pemain:\n1. 2 pemain\n2. 3 pemain\n3. 4 pemain\n>"))

    while choice > 3 or choice < 1:
        print("Masukkan Anda salah.Pilih sesuai nomor yang ada, jika ingin 2 pemain input 1, dst.")
        choice = int(input("Pilihlah jumlah pemain:\n1. 2 pemain\n2. 3 pemain\n3. 4 pemain\n>"))

    n = choice + 1
    arrUsername = []
    for i in range(n):
        playerUsername = input(f"Masukkan Username player ke {i + 1}:\n>")
        arrUsername.append(playerUsername)
        dict[playerUsername] = [i, base_money, curr_pos]

    turn = createTurn(arrUsername)

    return dict, turn

def diceRoll():
    # Implementasi kelompok I 
    print("ROLLING...")
    dice1, dice2 = randint(1, 6), randint(1, 6)
    displayRoll(dice1, dice2)
    print(f"Jumlah pengocokan dadu adalah:{dice1 + dice2}")
    return dice1 + dice2

def movePlayer(playerData, player, total_block, n_x, startData, screen, mapping):
    move = diceRoll()
    curr_position = playerData[player][2]
    #Update position
    next_post = (curr_position + move) % total_block
    playerData[player][2] = next_post

    # Display the position of the player
    player = padding(player, n_x - 2)

    
    # Display Movement

    start_x, y = startData[mapping[curr_position]]
    flag = False 

    # if there are other character in the same block
    for (username, (i, base_money, curr_pos)) in playerData.items():
        if curr_pos == curr_position:
            username = padding(username, n_x - 2)
            modifyScreen(start_x, y + 1, screen, username)
            flag = True 
            break 

    # If curr block is empty, remove the username
    if not flag:
        modifyScreen(start_x, y + 1, screen, padding("", n_x - 2))
    
    # Write player in next block
    start_x, y = startData[mapping[next_post]]
    modifyScreen(start_x, y + 1, screen, player)

    # Display the new screen
    Display(screen)

    return next_post

def checkCity(curr_position, cityData):
    #Check if a place has an owner or not
    owner = cityData[curr_position][7]
    if owner == "":
        return False 

    else:
        return True

def cityPayAmount(cityData, curr_pos, costType):
    if costType == "buy":
        base_price = cityData[curr_pos][3][0]

    if costType == "upgrade":
        base_price = cityData[curr_pos][2][0]

    cityType = cityData[curr_pos][5]

    if cityType == 1:
        multiplier = 2.45
        return [base_price, round(base_price * (1 + multiplier)), round(base_price * (1 + 2 * multiplier))]

    elif cityType == 2:
        multiplier = 1.45
        return [base_price, round(base_price * (1 + multiplier**(1.5))), round(base_price * (1 + (2 * multiplier)**(1.5)))]

    elif cityType == 3:
        multiplier = 1.225
        return [base_price, round(base_price * (1 + multiplier**(2.2))), round(base_price * (1 + (2 * multiplier)**(2.2)))]

def buy(curr_pos, cityData, playerData, player, startData, mapping, screen, n_x):
    payAmount = cityPayAmount(cityData, curr_pos, costType="buy")
    choice = input(f"Apakah Anda Ingin membeli rumah di kota {cityData[curr_pos][0]}?(Y/N)\n>")

    while choice != "Y" and choice != "y" and choice != "n" and choice != "N":
        print("Masukkan Anda salah.")
        choice = input(f"Apakah Anda Ingin membeli rumah di kota {cityData[curr_pos][0]}?(Y/N)\n>")

    if choice == "Y" or choice == "y":
        playerMoney = playerData[player][1]

        print(f"UANG ANDA: {playerMoney}")
        print("Pilih Berapa rumah yang ingin Anda beli")
        count = 0
        payAmount = [pay for pay in payAmount if pay <= playerMoney]

        if len(payAmount) > 0:
            for pay in payAmount:
                print(f"{count + 1}. {count + 1} rumah : {pay}")
                count += 1

            choice = int(input("Pilihan mana yang ingin Anda Beli?\n>"))

            while choice < 0  or choice - 1 > count - 1:
                print("Masukkan Anda Salah!")
                choice = int(input("Pilihan mana yang ingin Anda Beli?\n>"))

            # Update game
            # Decrease player money, Add Ownership, Update city level, Update all necessary cost to the corresponding level, update the screen
            playerMoney -= payAmount[choice - 1]
            playerData[player][1] = playerMoney

            cityData[curr_pos][6] = choice
            cityData[curr_pos][7] = player
            updateCost(curr_pos, cityData)

            start_x, y = startData[mapping[curr_pos]]
            text1 = padding(player, n_x - 2)
            text2 = padding(str(int(cityData[curr_pos][1][1])), n_x - 2)
            modifyScreen(start_x, y + 2, screen, text1)
            modifyScreen(start_x, y + 3, screen, text2)

            print(f"Uang Anda sisa : {playerMoney}")

        else:
            print("Uang Anda tidak Cukup.")

def pay(curr_pos, cityData, player, playerData, TransformMap, screen, n_x, startData):
    owner = cityData[curr_pos][7]
    is_bankrupt = False 

    if owner != player:
        print("Anda masuk ke area yang telah dibeli.")
        rent_fee = cityData[curr_pos][1][1]

        print(f"Harga sewa di kota {cityData[curr_pos][0]} adalah {rent_fee}")
        playerMoney = playerData[player][1]

        if playerMoney > rent_fee:
            playerMoney -= rent_fee
            playerData[player][1] = playerMoney

        else:
            is_bankrupt = sell(rent_fee, cityData, player, playerData, curr_pos, startData, TransformMap, n_x, screen)

        playerData[owner][1] = playerData[owner][1] + rent_fee

        print(f"Uang player {owner} bertambah sebesar {rent_fee} menjadi {playerData[owner][1]}")

        if not is_bankrupt:
            print(f"Uang player {player} sisa : {playerMoney}")

            changeOwnership(curr_pos, cityData, player, playerData, TransformMap, screen, n_x, startData)

    return is_bankrupt


def sell(rent, cityData, player, playerData, curr_pos, startArr, mapping, n_x, screen):
    ownedProperty = []
    playerMoney = playerData[player][1]

    for i in range(len(cityData)):
        if cityData[i][7] == player:
            ownedProperty.append(i)

    worth = 0

    for item in ownedProperty:
        worth += cityData[item][4][1]

    if (worth + playerMoney) < rent:
        bankrupt(player, playerData, cityData, ownedProperty, curr_pos, startArr, mapping, n_x, screen)
        return True

    else:
        print("Pilih rumah yang ingin Anda jual!")
        for i in range(len(ownedProperty)):
            data = cityData[ownedProperty[i]]
            print(f"{i + 1}. {data[0]} : {data[4][1]}")

        arrChoice = input("Masukkan pilihan - pilihan Anda\n>").split()
        sellAmount = playerMoney

        for choice in arrChoice:
            sellAmount += cityData[ownedProperty[int(choice) - 1]][4][1]

        while sellAmount < rent:
            print("Harap pilih properti yang lain yang ingin dijual, uang masih belum mencukupi.")
            arrChoice = input("Masukkan pilihan - pilihan Anda\n>").split()
            sellAmount = playerMoney

            for choice in arrChoice:
                sellAmount += int(cityData[ownedProperty[int(choice) - 1]][4][1])

        #update game
        playerMoney = sellAmount - rent 
        playerData[player][1] = playerMoney
        

        for choice in arrChoice:
            data = cityData[ownedProperty[int(choice) - 1]]
            #delete ownership
            data[7] = ''
            #restart level and price
            data[6] = 1
            data[4][1] = 0
            data[3][1] = 0
            data[2][1] = 0
            data[1][1] = 0
            start_x, y = startArr[mapping[ownedProperty[int(choice) - 1]]]
            text1 = padding("", n_x - 2)
            text2 = padding(str(data[1][0]), n_x - 2)
            modifyScreen(start_x, y + 2, screen, text1) 
            modifyScreen(start_x, y + 3, screen, text2)

    return False


def bankrupt(player, playerData, cityData, ownedProperty, curr_pos, startArr, mapping, n_x, screen):
    # Remove all player city and revert the data back 
    for item in ownedProperty:
        data = cityData[item]
        #delete ownership
        data[7] = ''
        #restart level and price
        data[6] = 1
        data[4][1] = 0
        data[3][1] = 0
        data[2][1] = 0
        data[1][1] = 0 
        start_x, y = startArr[mapping[item]]
        price = padding(str(data[4][0]), n_x - 2)
        owner = padding("", n_x - 2)
        modifyScreen(start_x, y + 2, screen, owner)
        modifyScreen(start_x, y + 3, screen, price)

    start_x, y = startArr[mapping[curr_pos]]
    owner = padding("", n_x - 2)
    modifyScreen(start_x, y + 1, screen, owner)

    #Remove player data
    del playerData[player]

    # Remove character in screen
    text = padding("", n_x - 2)
    modifyScreen(start_x, y + 1, screen, text)


    print(f"{player} telah bankrut! Sehingga dikeluarkan dari permainan. Better luck next time!")            

def changeOwnership(curr_pos, cityData, player, playerData, mapping, screen, n_x, startData):
    playerMoney = playerData[player][1]
    print(f"Uang Anda sekarang berjumlah: {playerMoney}")

    choice = input("Apakah Anda ingin membeli kota ini?(Y/N)\n>")

    while choice != "Y" and choice != "y" and choice != "n" and choice != "N":
        print("Masukkan Anda salah.")
        choice = input(f"Apakah Anda Ingin membeli rumah di kota {cityData[curr_pos][0]}?(Y/N)\n>")

    if choice == "Y" or choice == "y":
        data = cityData[curr_pos]
        cityType = data[5]
        if cityType == 1:
            k = 1.015

        elif cityType == 2:
            k = 1.199

        elif cityType == 3:
            k = 1.345
        
        fee = round (k * data[3][1])

        if playerMoney > fee:
            playerData[player][1] -= fee
            print(f"Saldo {player} sekarang sisa {playerData[player][1]}")

            playerData[data[7]][1] += fee
            print(f"Saldo {data[7]} sekarang bertambah menjadi {playerData[data[7]][1]}")

            data[7] = player

            start_x, y = startData[mapping[curr_pos]]
            text1 = padding(player, n_x - 2)
            modifyScreen(start_x, y + 2, screen, text1)

        else:
            print("Uang Anda kurang dari saldo.")

def upgrade(curr_pos, cityData, player, playerData):
    owner = cityData[curr_pos][7]
    playerMoney = playerData[player][1]

    if owner == player:
        choice = input(f"Apakah Anda ingin membeli rumah yang baru di kota {cityData[curr_pos][0]}?(Y/N)\n>")

        while choice != "Y" and choice != "y" and choice != "n" and choice != "N":
            print("Masukkan Anda salah.")
            choice = input(f"Apakah Anda ingin membeli rumah yang baru di kota {cityData[curr_pos][0]}?(Y/N)\n>")

        if choice == "Y" or choice == "y":
            curr_lvl = cityData[curr_pos][6]

            if curr_lvl < 3:
                payAmout = cityPayAmount(cityData, curr_pos, costType="upgrade")
                availableUpgrade = [payAmout[i] for i in range(len(payAmout)) if (curr_lvl<= i < 3 and payAmout[i] <= playerMoney)]

                count = 0
                if len(availableUpgrade) > 0:
                    for upgrade in availableUpgrade:
                        print(f"{count + 1}. Penambahan menjadi {curr_lvl + count + 1} rumah : {upgrade}")
                        count += 1

                    choice = int(input("Pilihan upgrade yang diinginkan?\n>"))

                    playerMoney -= availableUpgrade[choice - 1]
                    playerData[player][1] = playerMoney

                    cityData[curr_pos][6] += choice
                    updateCost(curr_pos, cityData)
                    
                else:
                    print("Uang Anda tidak cukup.")
            else:
                print("Tidak Ada Upgrade yang tersedia")

def updateCost(curr_pos, cityData):
    cityType = cityData[curr_pos][5]
    lvl = cityData[curr_pos][6]

    if cityType == 1:
        multiplier = 1.875
        for i in range(1, 5):
            cityData[curr_pos][i][1] = round(cityData[curr_pos][i][0] * (1 + multiplier * (lvl - 1)))

    elif cityType == 2:
        multiplier = 1.375
        for i in range(1, 5):
            cityData[curr_pos][i][1] = round(cityData[curr_pos][i][0] * (1 + (multiplier * (lvl - 1))**1.5))

    elif cityType == 3:
        multiplier = 1.225
        for i in range(1, 5):
            cityData[curr_pos][i][1] = round(cityData[curr_pos][i][0] * (1 + (multiplier * (lvl - 1))**1.5))

        
