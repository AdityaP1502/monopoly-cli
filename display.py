# Library to display board 
def addTextInSquare(text, n):
    arrText = padding(text, n)
    arrMiddle = ["*"] + [char for char in arrText] + ["*"] + [" "]

    return arrMiddle

def gap(arr, n, k, flag):
    if flag:
        return arr + [" " for i in range((k - 2) * (n + 1))] + arr

    else:
        return k * arr

def gridTxtHandler(arrOfText, textStart, j, n, k, flag):
    if flag:
        # Only two squares, one at left and one at right
        arr_left = addTextInSquare(arrOfText[textStart][j], n - 2)
        arr_right = addTextInSquare(arrOfText[textStart + 1][j], n - 2)

        return arr_left + [" " for i in range((k - 2) * (n + 1))] + arr_right

    else:
        arr = []

        for i in range(k):
            arr += addTextInSquare(arrOfText[textStart + i][j], n - 2)

        return arr 

def createSquare(start, n, m, k, arrOfText, gapFlag, screen):
    arrTop = (["*" for i in range(n)] + [" "])
    arrTop = gap(arrTop, n, k, gapFlag)
    screen.append(arrTop)

    for i in range(m):
        arrMiddle = gridTxtHandler(arrOfText, start, i, n, k, gapFlag)
        screen.append(arrMiddle)

    screen.append(arrTop[:])
    

def createGrid(n_x, k_x, n_y, k_y, arrOfText, screen):
    start = 0
    createSquare(start, n_x, n_y, k_x, arrOfText, False, screen)
    start += k_x

    for i in range(k_y):
        createSquare(start, n_x, n_y, k_x, arrOfText, True, screen)
        start += 2

    createSquare(start, n_x, n_y, k_x, arrOfText, False, screen)

def Display(screen):
    for i in range(len(screen)):
        for j in range(len(screen[0])):
            print(screen[i][j], end='')
        print()

def Screen(n_x, k_x, n_y, k_y, arrOfText):
    screen = []
        
    createGrid(n_x, k_x, n_y, k_y, arrOfText, screen)
    modifyScreen(round(k_x / 2 * n_x) - 3, n_y + 2, screen, "MONOPOLI")
    modifyScreen(round(k_x / 2 * n_x) - 2, n_y + 3, screen, "KELAS 1")
    return screen

def modifyScreen(start_x, y, screen, text):

    for i in range(len(text)):
        screen[y][start_x + i] = text[i]

def createDice(dice):
    diceDisplay = [["  ", "  ", "  "],["  ", "  ", "  "],["  ", "  ", "  "]]
    if dice == 1:
        diceDisplay[1][1] = "* "
        
    elif dice == 2:
        diceDisplay[0][0] = "* "
        diceDisplay[2][2] = "* "

    elif dice == 3:
        diceDisplay[0][0] = "* "
        diceDisplay[1][1] = "* "
        diceDisplay[2][2] = "* "

    elif dice == 4:
        diceDisplay[0][0] = "* "
        diceDisplay[0][2] = "* "
        diceDisplay[2][0] = "* "
        diceDisplay[2][2] = "* "

    elif dice == 5:
        diceDisplay[0][0] = "* "
        diceDisplay[0][2] = "* "
        diceDisplay[1][1] = "* "
        diceDisplay[2][0] = "* "
        diceDisplay[2][2] = "* "

    elif dice == 6:
        for i in range(3):
            diceDisplay[i][0] = "* "
            diceDisplay[i][2] = "* "

    #ADD BORDER
    for i in range(3):
        diceDisplay[i] = ["# "] + diceDisplay[i] + ["# "]

    return [["# ", "# ", "# ", "# ", "# "]] + diceDisplay + [["# ", "# ", "# ", "# ", "# "]]

        
def displayRoll(dice1, dice2):
    diceDisplay1 = createDice(dice1)
    diceDisplay2 = createDice(dice2)

    for i in range(5):
        display = diceDisplay1[i] + diceDisplay2[i]

        for char in display:
            print(char, end="")

        print()

def startArr(k_x, k_y, n_x, n_y):
    arr = []

    pos_x = 1
    pos_y = 1

    for i in range(k_x):
        arr.append((pos_x, pos_y))
        pos_x +=  n_x + 1

    pos_x = 1
    pos_y = 1 + (n_y + 2)
    for j in range(k_y):
        arr.append((pos_x, pos_y))
        pos_x = 1 + (k_x - 1) * (n_x + 1)
        arr.append((pos_x, pos_y))
        pos_y += n_y + 2 

    pos_x = 1
    for i in range(k_x):
       arr.append((pos_x, pos_y))
       pos_x +=  n_x + 1  

    return arr
    
def padding(text, max_length):
    length = len(text)

    if length > max_length:
        arrText = [text[i] for i in range(max_length)]

    elif length < max_length:
        dif = max_length - length
        totalPadLeft = dif // 2
        totalPadRight = dif - totalPadLeft
        arrText = [" " for i in range(totalPadLeft)] + [char for char in text] + [" " for i in range(totalPadRight)]

    else:
        arrText = text

    return arrText

def mapping(k_x, k_y):
    dict = {}

    for i in range(k_x):
        dict[(k_y + 1) + i] = i

    i = k_x

    for j in range((k_y), 0, -1): 
        dict[j] = i
        dist = 2 * ((k_y + 1) - j) + (k_x - 1)
        dict[j + dist] = i + 1
        i += 2 

    dict[0] = i 
    base_dist = 2 * (k_y + 1) + (k_x)
    i += 1

    for k in range(k_x - 1):
        dict[base_dist - k] = i 
        i += 1

    return dict

def createArrOfText(cityData, mapping):
    n = len(cityData)
    arrOfText = [["","","",""] for i in range(n)]

    for i in range(n):
        j = mapping[i]
        arrOfText[j][0] = cityData[i][0]
        arrOfText[j][2] = cityData[i][7]
        arrOfText[j][3] = str(cityData[i][1][1])

    return arrOfText

if __name__ == "__main__":
    arrOfText = [["JAKARTA", "", "","100.000"], ["MAKASSAR", "", "", "200.000"], ["MAKASSAR", "", "", "200.000"], ["MAKASSAR", "", "", "200.000"], ["MAKASSAR", "", "", "200.000"], ["MAKASSAR", "", "", "200.000"], ["MAKASSAR", "", "", "200.000"], ["MAKASSAR", "", "", "200.000"]]
    n_x = 16
    n_y = 4
    k_x = 3
    k_y = 1

    screen = Screen(n_x, k_x, n_y, k_y, arrOfText)
    Display(screen)

    dice1 = 6
    dice2 = 3
    displayRoll(dice1, dice2)
