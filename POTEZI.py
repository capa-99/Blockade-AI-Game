import copy

#startne pozicije x: ▓▓▓
#startne pozicije o: ░░░
#x: × 
#o: ○

#tabela je predstavljena kao matrica
#elementi matrice su liste od 3 elemenata [polje, desni zid polja, donji zid polja]
#polje: 0 - prazno, ▓▓▓, ░░░ - startne pozicije,  ○ ,  × - figure
 
# table = [
#     [ [0,'|','───'], ["▓▓▓",'|','───'], [0,'|','───'], ["░░░",'|','───'], [0,'ǁ','───'] ],
#     [ [0,'ǁ','───'], [0,'|,'───'], [0,'|','───'], [0,'|','───'], [" ○ ",'ǁ','───'] ],
#     [ [0,'ǁ','═══'], ["░░░",'|','═══'], [0,'|','───'], [0,'|','───'], [0,'ǁ','───'] ],
#     [ [0,'|','───'], [0,'|','───'], ["▓▓▓",'|','───'], [" ■ ",'|','───'], [0,'ǁ','───'] ],
#     [ [0,'|','═══'], [0,'|','═══'], [0,'|','═══'], [0,'|','═══'], [0,'ǁ','═══'] ]
# ]

table = []

#informacije o igri
info = {
    "dimensions" : [0, 0], #dimenzije tabele
    "start_position_x" : {'x1':[0, 0],  'x2':[0, 0]}, #startne pozicije za x
    "start_position_o" :  {'o1':[0, 0],  'o2':[0, 0]}, #startne pozicije za o
    "player_position_x" :  {'x1':[0, 0],  'x2':[0, 0]}, #pozicije figura za x
    "player_position_o" :  {'o1':[0, 0],  'o2':[0, 0]}, #pozicije figura za o
    "player_x_wall_number" : [0, 0], #broj vertikalnih i horizontalnih zidova za x
    "player_o_wall_number" : [0, 0], #broj vertikalnih i horizontalnih zidova za o
    "player_turn" : "x", #ko je na potezu
    "ai" : "o", 
    "player" : "x"
}

##################################### NOVA IGRA, definisanje parametara ########################
def runGame():
    game = 1
    while game: #dok igrac ne unese 0
        newGame()
        while not isEndGame(): #odigravaju se potezi dok se ne ispune uslovi gotove igre
            play()
    
        print('')
        print('█▀▀ ▄▀█ █▀▄▀█ █▀▀   █▀█ █░█ █▀▀ █▀█')
        print('█▄█ █▀█ █░▀░█ ██▄   █▄█ ▀▄▀ ██▄ █▀▄')
        print('\n')
    
        game = int(input("Nova igra? (1 - Da, 0 - Ne) "))
        deleteTable()

def newGame():

    print('')
    print('   ██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░█████╗░██████╗░███████╗')
    print('   ██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔══██╗██╔══██╗██╔════╝')
    print('   ██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░███████║██║░░██║█████╗░░')
    print('   ██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░██╔══██║██║░░██║██╔══╝░░')
    print('   ██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██║░░██║██████╔╝███████╗')
    print('   ╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚══════╝')
    print('')
    print('    █▄▄ █▄█ ▀  █▀▀ █░█ █▀█ █░░ █▄█   █▄▄ █▀█ ▄▀█ █▀▀ █▄▀ █▀▀ ▀█▀ █▀')
    print('    █▄█ ░█░ ▄  █▄▄ █▄█ █▀▄ █▄▄ ░█░   █▄█ █▀▄ █▀█ █▄▄ █░█ ██▄ ░█░ ▄█')
    setGameConfig() 
    setStartPosition() 
    createTable()
    drawTable(table)


def setTableDimensions():

    print("\nUnesite dimenzije table: ")
    print("(minimalne dimenzije 14x11, maksimalne dimenzije 28x22)")
    m = int(input("sirina: "))
    n = int(input("visina: "))

    #if n >= 11 and n <= 22 and m >= 14 and m <= 28: 
    if n >= 1 and n <= 22 and m >= 1 and m <= 28: 
        info["dimensions"][0] = n
        info["dimensions"][1] = m
        print("Generisace se tabla dimenzija (", m, "x", n, ").")
        return True
    else:
        return False

def setWallNumber():

    walls = int(input("\nUnesite broj zidova\n(minimalan broj zidova 9, maksimalan 18): "))
    
    #if walls >= 9 and walls <= 18:
    if walls >= 1 and walls <= 18: # Zbog algoritma
        info["player_x_wall_number"][0] = walls
        info["player_x_wall_number"][1] = walls
        info["player_o_wall_number"][0] = walls
        info["player_o_wall_number"][1] = walls
        print("Svaki igrac posedovace ", walls, " plavih i zelenih zidova.")
        return True
    else:
        return False

def setFirstPlayer():

    first = input("\nIzaberite igraca \n(X ili O, X igra prvi): ")

    if first == "x":
        print("Vi igrate prvi.")
        info["player_turn"] = 'x'
        info["player"] = "x"
        info["ai"] = "o"
        return True
    elif first == "o":
        print("Protivnik igra prvi.")
        info["player"] = "o"
        info["player_turn"] = 'x'
        info["ai"] = "x"
        return True
    else:
        return False

def setGameConfig():

    while not setTableDimensions():
        print("Nevalidne dimenzije! Unesite ponovo")
        
    while not setWallNumber():
        print("Nevalidan broj zidova! Unesite ponovo")

    while not setFirstPlayer():
        print("Nevalidan odabir! Unesite ponovo")

def setStartPosition():
    #ravnomerno rasporedjivanje startnih pozicija
    partn = (info["dimensions"][1] - 2) // 4 
    partm = (info["dimensions"][0] - 2) // 3
    #pozicija gornje startne pozicije za x
    info["start_position_x"]['x1'][0] = partn 
    info["start_position_x"]['x1'][1] = partm
    #pozicija gornje startne pozicije za o
    info["start_position_o"]['o1'][0] = partn
    info["start_position_o"]['o1'][1] = info["dimensions"][1] - partm - 1
    #pozicija donje startne pozicije za x
    info["start_position_x"]['x2'][0] = info["dimensions"][0] - partn - 1 
    info["start_position_x"]['x2'][1] = partm
    #pozicija donje startne pozicije za o
    info["start_position_o"]['o2'][0] = info["dimensions"][0] - partn - 1
    info["start_position_o"]['o2'][1] = info["dimensions"][1] - partm - 1
    
    #postavljanje figura na startne pozicije
    info["player_position_x"]['x1'][0] = info["start_position_x"]['x1'][0]
    info["player_position_x"]['x1'][1] = info["start_position_x"]['x1'][1]
    info["player_position_x"]['x2'][0] = info["start_position_x"]['x2'][0]
    info["player_position_x"]['x2'][1] = info["start_position_x"]['x2'][1]
    info["player_position_o"]['o1'][0] = info["start_position_o"]['o1'][0]
    info["player_position_o"]['o1'][1] = info["start_position_o"]['o1'][1]
    info["player_position_o"]['o2'][0] = info["start_position_o"]['o2'][0]
    info["player_position_o"]['o2'][1] = info["start_position_o"]['o2'][1]

#################################### PROVERA VALIDNOSTI UNETIH INFORMACIJA ######################
def checkForWalls(cell_i, cell_j, player_i, player_j, table): #FAZA II - potrebno proslediti tablu kao parametar
    #proverava za svaki potez da li postoji zid izmedju
    if cell_i == player_i and cell_j == (player_j - 2): #potez levo
        if table[player_i][player_j - 1][1] == 'ǁ' or table[player_i][player_j - 2][1] == 'ǁ':
            return False
        else:
            return True

    elif cell_i == (player_i + 2) and cell_j == player_j: #potez dole
        if table[player_i][player_j][2] == '═══' or table[player_i + 1][player_j][2] == '═══':
            return False
        else:
            return True

    elif cell_i == player_i and cell_j == (player_j + 2): #potez desno
        if table[player_i][player_j][1] == 'ǁ' or table[player_i][player_j + 1][1] == 'ǁ':
            return False
        else:
            return True

    elif cell_i == (player_i - 2) and cell_j == player_j: #potez gore
        if table[player_i - 1][player_j][2] == '═══' or table[player_i - 2][player_j][2] == '═══':
            return False
        else:
            return True

    elif cell_i == (player_i - 1) and cell_j == (player_j - 1): #potez levo-gore
        if (table[player_i][player_j - 1][1] == 'ǁ' and table[player_i - 1][player_j][2] == '═══') or (table[player_i - 1][player_j - 1][1] == 'ǁ' and table[player_i - 1][player_j - 1][2] == '═══') or (table[player_i - 1][player_j - 1][2] == '═══' and table[player_i - 1][player_j][2] == '═══') or (table[player_i - 1][player_j - 1][1] == 'ǁ' and table[player_i][player_j - 1][1] == 'ǁ'):
            return False
        else:
            return True

    elif cell_i == (player_i + 1) and cell_j == (player_j - 1): #potez levo-dole
        if (table[player_i][player_j - 1][1] == 'ǁ' and table[player_i][player_j][2] == '═══') or (table[player_i + 1][player_j - 1][1] == 'ǁ' and table[player_i][player_j - 1][2] == '═══') or (table[player_i][player_j][2] == '═══' and table[player_i][player_j - 1][2] == '═══') or (table[player_i][player_j - 1][1] == 'ǁ' and table[player_i + 1][player_j - 1][1] == 'ǁ'):
            return False
        else:
            return True

    elif cell_i == (player_i - 1) and cell_j == (player_j + 1): #potez desno-gore
        if (table[player_i][player_j][1] == 'ǁ' and table[player_i - 1][player_j][2] == '═══') or (table[player_i - 1][player_j][1] == 'ǁ' and table[player_i - 1][player_j + 1][2] == '═══') or (table[player_i - 1][player_j][2] == '═══' and table[player_i - 1][player_j + 1][2] == '═══') or (table[player_i - 1][player_j][1] == 'ǁ' and table[player_i][player_j][1] == 'ǁ'):
            return False
        else:
            return True

    elif cell_i == (player_i + 1) and cell_j == (player_j + 1): #potez desno-dole
        if (table[player_i + 1][player_j][1] == 'ǁ' and table[player_i][player_j + 1][2] == '═══') or (table[player_i][player_j][1] == 'ǁ' and table[player_i][player_j][2] == '═══') or (table[player_i][player_j][2] == '═══' and table[player_i][player_j + 1][2] == '═══') or (table[player_i][player_j][1] == 'ǁ' and table[player_i + 1][player_j][1] == 'ǁ'):
            return False
        else:
            return True

    #specijalan slucaj kada se skace samo 1 polje
    elif cell_i == player_i and cell_j == (player_j - 1): #potez levo
        if table[player_i][player_j - 1][1] == 'ǁ':
            return False
        else:
            return True

    elif cell_i == (player_i + 1) and cell_j == player_j: #potez dole
        if table[player_i][player_j][2] == '═══':
            return False
        else:
            return True

    elif cell_i == player_i and cell_j == (player_j + 1): #potez desno
        if table[player_i][player_j][1] == 'ǁ':
            return False
        else:
            return True

    elif cell_i == (player_i - 1) and cell_j == player_j: #potez gore
        if table[player_i - 1][player_j][2] == '═══':
            return False
        else:
            return True

def checkPlayerPosition(player_i, player_j):

    #proveravanje koju je figuru izabrao igrac
    if info["player_turn"] == "x":
        if player_i == info['player_position_x']['x1'][0] and player_j == info['player_position_x']['x1'][1]:
            return 'x1'
            
        elif player_i == info['player_position_x']['x2'][0] and player_j == info['player_position_x']['x2'][1]:
            return 'x2'
        else:
            return None
    else:
        if player_i == info['player_position_o']['o1'][0] and player_j == info['player_position_o']['o1'][1]:
            return 'o1'
        elif player_i == info['player_position_o']['o2'][0] and player_j == info['player_position_o']['o2'][1]:
            return 'o2'
        else:
            return None
            
def checkPlayerMove(cell_i, cell_j, player_i, player_j, player_move, info, table):#FAZA II - potrebno proslediti tablu i info (tekuce stanje) kao parametar
    #proverava razne slucajeve i granicne vrednosti kako bi se proverila validnost poteza
    #FAZA II - umesto true/false funkcija vraca broj koji odredjuje koji slucaj je u pitanju
    if cell_i < 0 or cell_i >= info["dimensions"][0] or cell_j < 0 or cell_j >= info["dimensions"][1]: 
        return 1 #NEVALIDNO, indeksi van granica tabele
    else:
        #regularni potezi
        if (cell_i == player_i and cell_j == (player_j - 2)) or (cell_i == (player_i + 2) and cell_j == player_j) or (cell_i == player_i and cell_j == (player_j + 2)) or (cell_i == (player_i - 2) and cell_j == player_j) or (cell_i == (player_i - 1) and cell_j == (player_j - 1)) or (cell_i == (player_i + 1) and cell_j == (player_j - 1)) or (cell_i == (player_i - 1) and cell_j == (player_j + 1)) or (cell_i == (player_i + 1) and cell_j == (player_j + 1)):
            if (cell_i == info["player_position_x"]['x1'][0] and cell_j == info["player_position_x"]['x1'][1] and info["player_position_x"]['x1'][0] != info["start_position_x"]['x1'][0] and info["player_position_x"]['x1'][1] != info["start_position_x"]['x1'][1]) or (cell_i == info["player_position_x"]['x2'][0] and cell_j == info["player_position_x"]['x2'][1] and info["player_position_x"]['x2'][0] != info["start_position_x"]['x2'][0] and info["player_position_x"]['x2'][1] != info["start_position_x"]['x2'][1]) or (cell_i == info["player_position_o"]['o1'][0] and cell_j == info["player_position_o"]['o1'][1] and info["player_position_o"]['o1'][0] != info["start_position_o"]['o1'][0] and info["player_position_o"]['o1'][1] != info["start_position_o"]['o1'][1]) or (cell_i == info["player_position_o"]['o2'][0] and cell_j == info["player_position_o"]['o2'][1] and info["player_position_o"]['o2'][0] != info["start_position_o"]['o2'][0] and info["player_position_o"]['o2'][1] != info["start_position_o"]['o2'][1]):
                return 2 #NEVALIDNO, na ovom polju se vec nalazi figura
            
            elif (cell_i == info["player_position_x"]['x1'][0] and cell_j == info["player_position_x"]['x1'][1] and info["player_position_x"]['x1'][0] == info["start_position_x"]['x1'][0] and info["player_position_x"]['x1'][1] == info["start_position_x"]['x1'][1]) or (cell_i == info["player_position_x"]['x2'][0] and cell_j == info["player_position_x"]['x2'][1] and info["player_position_x"]['x2'][0] == info["start_position_x"]['x2'][0] and info["player_position_x"]['x2'][1] == info["start_position_x"]['x2'][1]) or (cell_i == info["player_position_o"]['o1'][0] and cell_j == info["player_position_o"]['o1'][1] and info["player_position_o"]['o1'][0] == info["start_position_o"]['o1'][0] and info["player_position_o"]['o1'][1] == info["start_position_o"]['o1'][1]) or (cell_i == info["player_position_o"]['o2'][0] and cell_j == info["player_position_o"]['o2'][1] and info["player_position_o"]['o2'][0] == info["start_position_o"]['o2'][0] and info["player_position_o"]['o2'][1] == info["start_position_o"]['o2'][1]):
                movePlayer(cell_i, cell_j, player_move, info)
                return 0#VALIDNO ako je figura protivnika na pocetnom stanju a igrac hoce da stane na njega

            elif not checkForWalls(cell_i, cell_j, player_i, player_j, table):
                return 3 #NEVALIDNO, ne moze se preskociti zid
            
            else:
                movePlayer(cell_i, cell_j, player_move, info)
                return 0 #VALIDNO
        #specijalni slucajevi kada je dozvoljeno da se igrac krece jedno polje
        elif ((cell_i == player_i and cell_j == (player_j - 1)) or (cell_i == (player_i + 1) and cell_j == player_j) or (cell_i == player_i and cell_j == (player_j + 1)) or (cell_i == (player_i - 1) and cell_j == player_j)) and checkForWalls(cell_i, cell_j, player_i, player_j, table):
            if info["player_turn"] == 'x' and ((cell_i == info["start_position_o"]['o1'][0] and cell_j == info["start_position_o"]['o1'][1]) or (cell_i == info["start_position_o"]['o2'][0] and cell_j == info["start_position_o"]['o2'][1])):
                movePlayer(cell_i, cell_j, player_move, info)
                return 0
            elif info["player_turn"] == 'o' and ((cell_i == info["start_position_x"]['x1'][0] and cell_j == info["start_position_x"]['x1'][1]) or (cell_i == info["start_position_x"]['x2'][0] and cell_j == info["start_position_x"]['x2'][1])):
                movePlayer(cell_i, cell_j, player_move, info)
                return 0
            elif (cell_i == player_i and cell_j == (player_j - 1)) and player_j - 2 >= 0:
                if (table[player_i][player_j - 2][0] != (0 and '░░░' and '▓▓▓')):
                    movePlayer(cell_i, cell_j, player_move, info)
                    return 0
            elif (cell_i == player_i and cell_j == (player_j + 1)) and player_j + 2 < info["dimensions"][1]:
                if (table[player_i][player_j + 2][0] != (0 and '░░░' and '▓▓▓')):
                    movePlayer(cell_i, cell_j, player_move, info)
                    return 0
            elif (cell_i == (player_i - 1) and cell_j == player_j) and player_i - 2 >= 0:
                if (table[player_i - 2][player_j][0] != (0 and '░░░' and '▓▓▓')):
                    movePlayer(cell_i, cell_j, player_move, info)
                    return 0
            elif (cell_i == (player_i + 1) and cell_j == player_j) and player_i + 2 < info["dimensions"][0]:
                if (table[player_i + 2][player_j][0] != (0 and '░░░' and '▓▓▓')):
                    movePlayer(cell_i, cell_j, player_move, info)
                    return 0
            else:
                return 4 #NEVALIDNO, figura ne moze da skoci na ovo polje
            
        else:
            return 4 #NEVALIDNO, figura ne moze da skoci na ovo polje

def checkIfValidWallDirection(wall):
    #proverava koji je zid izabrao igrac i da li mu je preostalo jos takvih zidova
    if wall != 1 and wall != 2:
        print("Nevalidan potez, nije ni horizontalno ni vertikalno")
        return False
    elif (wall == 1 and info["player_turn"] == 'x' and info["player_x_wall_number"][0] == 0) or (wall == 1 and info["player_turn"] == 'o' and info["player_o_wall_number"][0] == 0):
        print('Nemate vise vertikalnih zidova')
        return False
    elif (wall == 2 and info["player_turn"] == 'x' and info["player_x_wall_number"][1] == 0) or (wall == 1 and info["player_turn"] == 'o' and info["player_o_wall_number"][1] == 0):
        print("Nemate vise horizontalnih zidova")
        return False
    else:
        return True

def checkIfValidWallPosition(wall_i, wall_j, wall):
    #proveravanje ogranicenja za postavljanje zida
    if wall_i < 0 or wall_i > (info["dimensions"][0] - 2) or wall_j < 0 or wall_j > (info["dimensions"][1] - 2):
            #print("Nevalidan potez, indeksi van granica tabele")
            return 1
    else:
        if wall == 1: 
            if table[wall_i][wall_j][1] == 'ǁ' or table[wall_i + 1][wall_j][1] == 'ǁ':
                #print("Nevalidan potez, na ovom mestu je vec postavljen zid")
                return 2
            else:
                return 0
        else:
            if table[wall_i][wall_j][2] == '═══' or table[wall_i][wall_j + 1][2] == '═══':
                #print("Nevalidan potez, na ovom mestu je vec postavljen zid")
                return 2
            else:
                return 0

def convertStrToNum(str):
    #konc=vertuje string koji igrac unosi za koordinate u broj koji odgovara toj koordinati
    horizontal=['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S']
    for i in range(len(horizontal)):
        if str == horizontal[i]:
            return i 
    return -1

#################################### POTEZ #######################################################
def movePlayer(cell_i, cell_j, player_move, info): #FAZA II, poterbno proslediti info kao parametar
    #updatuje info ttako da sadrzi vrednosti odigranog poteza
    if info["player_turn"] == "x":
        info["player_position_x"][player_move][0] = cell_i
        info["player_position_x"][player_move][1] = cell_j               
    else:
        info["player_position_o"][player_move][0] = cell_i
        info["player_position_o"][player_move][1] = cell_j

def play():
    # JEDAN POTEZ I PROVERE SVIH OGRANICENJA
    #korisnik unosi sve vrednosti sve dok ne unese validne vrednosti
    print("\n Na potezu ste Vi, {}".format(info['player_turn']))

    tmpt = setANewState(table, info)
    ret = getAllPossibleMoves(info["player_turn"], tmpt[0], tmpt[1])
    print(ret)
    print(len(ret))
    

    print("Unesite poziciju figure sa kojom zelite da igrate: ")
    player_i = convertStrToNum(input('i: '))
    player_j = convertStrToNum(input('j: '))
    player_move = checkPlayerPosition(player_i, player_j)

    while player_move == None:
        print("Nevalidan unos pozicije igraca. Unesite ponovo!")
        print("Unesite poziciju figure sa kojom zelite da igrate: ")
        player_i = convertStrToNum(input('i: '))
        player_j = convertStrToNum(input('j: '))
        player_move = checkPlayerPosition(player_i, player_j)
        

    print("Unesite poziciju polja na koje zelite da pomerite figuru?")
    cell_i = convertStrToNum(input('i: '))
    cell_j = convertStrToNum(input('j: '))

    p = checkPlayerMove(cell_i, cell_j, player_i, player_j, player_move, info, table)
    while p :
        match(p):
            case 1:
                print("Nevalidan potez, indeksi van granica tabele") 
            case 2:
                print("Nevalidan potez, na ovom polju se vec nalazi figura")
            case 3:
                print("Nevalidan potez, ne moze se preskociti zid")
            case 4:
                print("Nevalidan potez, figura ne moze da skoci na ovo polje")

        print("Unesite poziciju polja na koje zelite da pomerite figuru?")
        cell_i = convertStrToNum(input('i: '))
        cell_j = convertStrToNum(input('j: '))
        p = checkPlayerMove(cell_i, cell_j, player_i, player_j, player_move, info, table)

 
    
    if (info["player_turn"] == 'x' and info["player_x_wall_number"][0] == 0 and info["player_x_wall_number"][1] == 0) or (info["player_turn"] == 'o' and info["player_o_wall_number"][0] == 0 and info["player_o_wall_number"][1] == 0):
        print("Nemate vise zidova")
        updateTableNoWalls(player_i, player_j, cell_i, cell_j, player_move, table, info)

    else:
        if info["player_turn"] == 'x':
            print("Preostalo Vam je: ", info["player_x_wall_number"][0], "vertikalnih i ", info["player_x_wall_number"][1], "horizontalnih zidova.")
        else:
            print("Preostalo Vam je: ", info["player_o_wall_number"][0], "vertikalnih i ", info["player_o_wall_number"][1], "horizontalnih zidova.")
        
        print("Koji zid zelite da postavite: ")
        print("1: vertikalni")
        print("2: horizontalini ")
        wall = int(input(''))

        while not checkIfValidWallDirection(wall):
            print("Koji zid zelite da postavite: ")
            print("1: vertikalni")
            print("2: horizontalini ")
            wall = int(input(''))

        print("Unesite poziciju polja za zid ?")
        wall_i = convertStrToNum(input('i: '))
        wall_j = convertStrToNum(input('j: '))

        temp = setANewState(table, info) #FAZA II - GENERISE SE NOVO STANJE
        updateTableOnlyWalls(wall, wall_i, wall_j, temp[0], temp[1])#FAZA II - u novo stanje dodaje se zid kojeg igrac zeli da postavi kako bi se proverilo da li on zatvara put

        w = checkIfValidWallPosition(wall_i, wall_j, wall)
        print(w)
        while w or not checkIfClosed(temp[0], temp[1]): #FAZA II - proverava se da li zid zatvara put
            if w == 1:
                print("Nevalidan potez, indeksi van granica tabele")
            elif w == 0:
                print("Nevalidan potez, zid zatvara put do cilja") 
            else:
                print("Nevalidan potez, na ovom mestu je vec postavljen zid")
            print("Unesite poziciju polja za zid ?")
            wall_i = convertStrToNum(input('i: '))
            wall_j = convertStrToNum(input('j: '))
            w = checkIfValidWallPosition(wall_i, wall_j, wall)
            temp = setANewState(table, info)
            updateTableOnlyWalls(wall, wall_i, wall_j, temp[0], temp[1])
        updateTableWithWalls(player_i, player_j, cell_i, cell_j, player_move, wall, wall_i, wall_j, table, info)

    drawTable(table)
    
    #promena ko je na potezu
    if info["player_turn"] == 'x':
        info["player_turn"] = 'o'
    else:
        info["player_turn"] = 'x'

def aiPlay():
    ######### PROBA ################
    #POTEZ AI, minmax algoritam
    print("\n Na potezu je AI, {}".format(info['player_turn']))
    minmax = setANewState(table, info)
    # if info["player_turn"] == "x":
    #     z = minimax((),"x", minmax[0], minmax[1], 2, 2)
    #     print(z)
    #     drawTable(z[0])
    # else:
    #     z = minimax((),"o", minmax[0], minmax[1], 2, 2)
    #     print(z)
    #     drawTable(z[0])

    smthng = minimaxAlphaBeta(minmax[0], minmax[1], 3, 3, (), minmax[1]["player_turn"], ((), 0), ((), 100))
    print(smthng)
    if info["ai"] == 'x':
        if smthng[1] == None:
            updateTableNoWalls(info["player_position_x"][smthng[0][0][2]][0], info["player_position_x"][smthng[0][0][2]][1], smthng[0][0][0], smthng[0][0][1], smthng[0][0][2], table)
        else:
            updateTableWithWalls(info["player_position_x"][smthng[0][0][2]][0], info["player_position_x"][smthng[0][0][2]][1], smthng[0][0][0], smthng[0][0][1], smthng[0][0][2], smthng[0][1][2], smthng[0][1][0], smthng[0][1][1], table, info)   
    else:
        if smthng[1] == None:
            updateTableNoWalls(info["player_position_o"][smthng[0][0][2]][0], info["player_position_o"][smthng[0][0][2]][1], smthng[0][0][0], smthng[0][0][1], smthng[0][0][2], table)
        else:
            updateTableWithWalls(info["player_position_o"][smthng[0][0][2]][0], info["player_position_o"][smthng[0][0][2]][1], smthng[0][0][0], smthng[0][0][1], smthng[0][0][2], smthng[0][1][2], smthng[0][1][0], smthng[0][1][1], table, info)   

    drawTable(table)
    if info["player_turn"] == 'x':
        info["player_turn"] = 'o'
    else:
        info["player_turn"] = 'x'

    ######### PROBA ################

############################### KRAJ IGRE ##########################################
def isEndGame():
    #proverava da li je kraj igre tako sto ispituje koordinate x i o
    if info["player_position_x"]["x1"][0] == info["start_position_o"]["o1"][0] and info["player_position_x"]["x1"][1] == info["start_position_o"]["o1"][1]:
        print("\nPobednik je X") # X1 je stao na polje O1
        return True
    elif info["player_position_x"]["x1"][0] == info["start_position_o"]["o2"][0] and info["player_position_x"]["x1"][1] == info["start_position_o"]["o2"][1]:
        print("\nPobednik je X") # X1 je stao na polje O2
        return True
    elif info["player_position_x"]["x2"][0] == info["start_position_o"]["o1"][0] and info["player_position_x"]["x2"][1] == info["start_position_o"]["o1"][1]:
        print("\nPobednik je X") # X2 je stao na polje O1
        return True
    elif info["player_position_x"]["x2"][0] == info["start_position_o"]["o2"][0] and info["player_position_x"]["x2"][1] == info["start_position_o"]["o2"][1]:
        print("\nPobednik je X") # X2 je stao na polje O2
        return True
    elif info["player_position_o"]["o1"][0] == info["start_position_x"]["x1"][0] and info["player_position_o"]["o1"][1] == info["start_position_x"]["x1"][1]:
        print("\nPobednik je O") # O1 je stao na polje X1
        return True
    elif info["player_position_o"]["o1"][0] == info["start_position_x"]["x2"][0] and info["player_position_o"]["o1"][1] == info["start_position_x"]["x2"][1]:
        print("\nPobednik je O") # O1 je stao na polje X2
        return True
    elif info["player_position_o"]["o2"][0] == info["start_position_x"]["x1"][0] and info["player_position_o"]["o2"][1] == info["start_position_x"]["x1"][1]:
        print("\nPobednik je O") # O2 je stao na polje X1
        return True
    elif info["player_position_o"]["o2"][0] == info["start_position_x"]["x2"][0] and info["player_position_o"]["o2"][1] == info["start_position_x"]["x2"][1]:
        print("\nPobednik je O") # O2 je stao na polje X2
        return True
    else:
        return False

############################### TABELA, CRUD, draw ###################################
def createTable():

    for i in range(info["dimensions"][0]):
        row = []
        for j in range(info["dimensions"][1]):
            cell = []
            ### proveravanje pozicija ###
            if (i == info["start_position_x"]['x1'][0] and j == info["start_position_x"]['x1'][1]) or (i == info["start_position_x"]['x2'][0] and j == info["start_position_x"]['x2'][1]):
                cell.append("▓×▓")
            elif (i == info["start_position_o"]['o1'][0] and j == info["start_position_o"]['o1'][1]) or (i == info["start_position_o"]['o2'][0] and j == info["start_position_o"]['o2'][1]):
                cell.append("░○░")
            else:
                cell.append(0)

            if j == info["dimensions"][1] - 1:
                cell.append('ǁ')
            else: 
                cell.append('|')

            if i == info["dimensions"][0] - 1:
                cell.append('═══')
            else: 
                cell.append('───')
            
            row.append(cell)
        table.append(row)
                
def updateTableWithWalls(old_i, old_j, new_i, new_j, player_move, wall_dir, wall_i, wall_j, table, info):
    
    updateTableNoWalls(old_i, old_j, new_i, new_j, player_move, table, info)
    updateTableOnlyWalls(wall_dir, wall_i, wall_j, table, info)

def updateTableOnlyWalls(wall_dir, wall_i, wall_j, table, info): #FAZA II - deo iz updateTableWithWalls prebacen ovde
    if info["player_turn"] == 'x': 
        if wall_dir == 1: #x postavlja vertikalni zid
            table[wall_i][wall_j][1] = 'ǁ'
            table[wall_i + 1][wall_j][1] = 'ǁ'
            info["player_x_wall_number"][0] = info["player_x_wall_number"][0] - 1
        else: #x postavlja horizontalni zid
            table[wall_i][wall_j][2] = '═══'
            table[wall_i][wall_j + 1][2] = '═══'
            info["player_x_wall_number"][1] = info["player_x_wall_number"][1] - 1

    else:
        if wall_dir == 1: #o postavlja vertikalni zid
            table[wall_i][wall_j][1] = 'ǁ'
            table[wall_i + 1][wall_j][1] = 'ǁ'
            info["player_o_wall_number"][0] = info["player_o_wall_number"][0] - 1
        else: #o postavlja horizontalno zid
            table[wall_i][wall_j][2] = '═══'
            table[wall_i][wall_j + 1][2] = '═══'
            info["player_o_wall_number"][1] = info["player_o_wall_number"][1] - 1

def updateTableNoWalls(old_i, old_j, new_i, new_j, player_move, table, info):

    if info["player_turn"] == 'x':
        #figura se pomera sa startne pozicije
        if old_i == info["start_position_x"][player_move][0] and old_j == info['start_position_x'][player_move][1]:
            table[old_i][old_j][0] = '▓▓▓'
            table[new_i][new_j][0] = " × "
        #figura se pomera na cilj
        elif (new_i == info["start_position_o"]['o1'][0] and new_j == info['start_position_o']['o1'][1]) or (new_i == info["start_position_o"]['o2'][0] and new_j == info['start_position_o']['o2'][1]):
            table[old_i][old_j][0] = 0 #polje na kome je bila figura je prazno
            table[new_i][new_j][0] = "░×░"
        #figura se pomera
        else:
            table[old_i][old_j][0] = 0 #polje na kome je bila figura je prazno
            table[new_i][new_j][0] = " × "

    else:
        #figura se pomera sa startne pozicije
        if old_i == info["start_position_o"][player_move][0] and old_j == info['start_position_o'][player_move][1]:
            table[old_i][old_j][0] = '░░░'
            table[new_i][new_j][0] = " ○ "
        #figura se pomera na cilj
        elif (new_i == info["start_position_x"]['x1'][0] and new_j == info['start_position_x']['x1'][1]) or (new_i == info["start_position_x"]['x2'][0] and new_j == info['start_position_x']['x2'][1]):
            table[old_i][old_j][0] = 0 #polje na kome je bila figura je prazno
            table[new_i][new_j][0] = "▓○▓"
        #figura se pomera
        else:
            table[old_i][old_j][0] = 0 #polje na kome je bila figura je prazno
            table[new_i][new_j][0] = " ○ "

def deleteTable():
    table.clear()

def drawTable(table): #FAZA II - potrebno proslediti tablu

    n = info["dimensions"][0]
    m = info["dimensions"][1]

    horizontal=(1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S');
    print("  ", end='')

    for i in range(m): #horizontalni brojevi gore 
        print("  ", end='') 
        print(horizontal[i], end='')
        print(' ', end='')
    print("")
    print("   ", end='')    

    for i in range(m): #gornji zidovi
        print('═══ ', end='')
    print("")

    for i in range(n):
        num = i #num - vertikalni brojevi levo
        print(horizontal[num], end='')
        print(' ǁ', end='')

        for j in range(m):
            el = ""
            if table[i][j][0] == 0:
                el = "   "
            else:
                el = table[i][j][0]
            el = el + table[i][j][1] #polje + desni zid
            print(el, end='')
        print(' ', end='')
        print(horizontal[num]) #vertikalni brojevi desno
        print("   ", end='')

        for j in range(m): #crtanje donjeg zida ispod polja table[i][j]
            print(table[i][j][2], end='')
            print(' ', end='')
        print("")
    print("  ", end='')

    for i in range(m):
        print("  ", end='')
        print(horizontal[i], end='')
        print(' ', end='')

    print("\n")
    print("x:", info["player_x_wall_number"][0], "V,", info["player_x_wall_number"][1], "H", ' ' * (n*3), "o:", info["player_o_wall_number"][0], "V,", info["player_o_wall_number"][1], "H")
    
#####################################################################################################    
########################################### FAZA II #################################################
#####################################################################################################

def checkIfClosedOneRoute(player, dest, table_tmp, info_tmp):
    path = findRoute(player, dest, table_tmp, info_tmp)
    if path == []: #ako je put prazan, znaci da je put pd player do dest zatvoren
        return False
    else:
        return True

def findRoute(player, dest, table_tmp, info_tmp):
    #A* algoritam, proverava da li postoji put od player(polje gde se nalazi jedna figura igraca) do dest (jedno od startnih pozicija protivnika)
    found_end = False #ukazuje da li je pronadjen ciljni cvor
    open_set = set() #set cvorova koje teba posetiti
    closed_set = set() #set posecenih cvorova
    g = {} #dict koji pamti stvarnu cenu puta od polaznog cvora do drugog cvora
    prev_nodes = {} #parovi cvorova oblika cvor:prethodnik
    g[player] = 0 #stvarna cena puta od player do player je 0
    prev_nodes[player] = None #player nema prethodnika
    open_set.add(tuple(player, )) #smesta se polazni cvor
    while len(open_set) > 0 and (not found_end): #sve dok imamo cvorove koji treba da se obrade i dok god se nije pronasao ciljni cvor
        node = None #ovde ce da se smesti cvor koji se obradjuje (sa najmanjom cenom)
        for next_node in open_set:
            if node is None or g[next_node] + hFunction(next_node, dest) < g[node] + hFunction(node, dest): #ako sledeci cvor ima manju ukupnu cenu puta onda prvo obradjujemo njega
                node = next_node #ovde ce biti cvor sa minimalnom ukupnom cenom puta
        if node[0] == dest[0] and node[1] == dest[1]: #ako smo dosli do cilja (ako se koordinate node i dest poklapaju)
            found_end = True
            break
        for destination in getAllPossibleMovesFigure(node, table_tmp, info_tmp): #obilaze se svi sledbenici od node (svi moguci potezi)
            if destination not in open_set and destination not in closed_set: #ako nije ni obradjen niti ceka na obradu
                open_set.add(destination) #dodaje se u open_set da se obradi
                prev_nodes[destination] = node #upisuje se prethodnik
                g[destination] = g[node] + 2 #stvarna cena puta, +2 jer su potezi duzine 2 (uglavnom)
                movePlayer(destination[0], destination[1], destination[2], info_tmp) # odigrava se potez na tabeli
                updateTableNoWalls(node[0], node[1], destination[0], destination[1], destination[2], table_tmp, info_tmp)

            elif g[destination] in open_set: #ako je cvor vec obradjen, mozda ima kraci put
                if g[destination] > g[node] + 2: #ako se desi da je novoizracunata cena manja, updatuje se 
                    g[destination] = g[node] + 2
                    prev_nodes[destination] = node
                    movePlayer(destination[0], destination[1], destination[2], info_tmp)
                    updateTableNoWalls(node[0], node[1], destination[0], destination[1], destination[2], table_tmp)                   
                        
        open_set.remove(node)
        closed_set.add(node)
    path = []
    if found_end:
        while prev_nodes[node] is not None: #konnstruisese put
            path.append(node)
            node = prev_nodes[node]
        path.append(player)
        path.reverse()
    return path

def getAllPossibleMovesFigure(player, table_tmp, info_tmp):
    #vraca sva polja (koordinate) na koje je moguce da player odigra potez
    all_moves= [(player[0] - 2, player[1], player[2]), (player[0] + 2, player[1], player[2]), 
                (player[0], player[1] - 2, player[2]), (player[0], player[1] + 2, player[2]),
                (player[0] - 1, player[1], player[2]), (player[0] + 1, player[1], player[2]),
                (player[0], player[1] - 1, player[2]), (player[0], player[1] + 1, player[2]),
                (player[0] - 1, player[1] - 1, player[2]), (player[0] - 1, player[1] + 1,player[2] ),
                (player[0] + 1, player[1] - 1, player[2]), (player[0] + 1, player[1] + 1, player[2])] #lista svih mogucih poteza
    l = []
    for x in all_moves:
        tmp = setANewState(table_tmp, info_tmp)
        if  not checkPlayerMove(x[0], x[1], player[0], player[1], player[2], tmp[1], tmp[0]) and checkForWalls(x[0], x[1], player[0], player[1], tmp[0]):
            l.append(x)
    return l #za svaki potez ispituje se da li je validan i vraca se samo ako jeste

def hFunction(node, dest):
    return abs(dest[0] - node[0]) + abs(dest[1] - node[1]) #razdaljina od dest do node kao pozitivan ceo broj koji oznacava broj polja koji razdvaja ova dva polja

def setANewState(table_tmp, info_tmp):
    #novo stanje, kreira se nova tabla i info dict i u njih se kopiraju vrednosti iz table i info koji su prosledjeni
    tabletemp = copy.deepcopy(table_tmp)
    infotemp = copy.deepcopy(info_tmp)
    retval = (tabletemp, infotemp)
    return retval

def checkIfClosed(table_tmp, info_tmp):
    #poziva checkIfClosedOneRoute (proverava da li postoji put izmedju 2 polja) za sve kombinacije ograca i startnih pozicija
    player_x1 = (info["player_position_x"]['x1'][0], info["player_position_x"]['x1'][1], 'x1')
    player_x2 = (info["player_position_x"]['x2'][0], info["player_position_x"]['x2'][1], 'x2')
    player_o1 = (info["player_position_o"]['o1'][0], info["player_position_o"]['o1'][1], 'o1')
    player_o2 = (info["player_position_o"]['o2'][0], info["player_position_o"]['o2'][1], 'o2')
    dest_x1 = (info["start_position_x"]['x1'][0], info["start_position_x"]['x1'][1])
    dest_x2 = (info["start_position_x"]['x2'][0], info["start_position_x"]['x2'][1])
    dest_o1 = (info["start_position_o"]['o1'][0], info["start_position_o"]['o1'][1])
    dest_o2 = (info["start_position_o"]['o2'][0], info["start_position_o"]['o2'][1])
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "x"
    if not checkIfClosedOneRoute(player_x1, dest_o1, temp[0], temp[1]): #x1->o1
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "x"
    if not checkIfClosedOneRoute(player_x1, dest_o2, temp[0], temp[1]):  #x1->o2
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "x"
    if not checkIfClosedOneRoute(player_x2, dest_o1, temp[0], temp[1]):  #x2->o1
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "x"
    if not checkIfClosedOneRoute(player_x2, dest_o2, temp[0], temp[1]):  #x2->o2
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "o"
    if not checkIfClosedOneRoute(player_o1, dest_x1, temp[0], temp[1]):  #o1->x1
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "o"
    if not checkIfClosedOneRoute(player_o1, dest_x2, temp[0], temp[1]):  #o1->x2
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "o"
    if not checkIfClosedOneRoute(player_o2, dest_x1, temp[0], temp[1]):  #o2->x1
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    temp = setANewState(table_tmp, info_tmp)
    temp[1]["player_turn"] = "o"
    if not checkIfClosedOneRoute(player_o2, dest_x2, temp[0], temp[1]):  #o2->x2
        #print("Nevalidan potez, zid zatvara put do cilja")
        return False
    return True

#####################################################################################################    
########################################### FAZA III ################################################
#####################################################################################################

def checkIfWallsAround(wall_i, wall_j, wall_dir, table_tmp, info_tmp):
    #proverava da li ima zidova koji dodiruju jedan zid 
    cnt = 0
    if wall_dir == 1:
        if (wall_i - 1) >= 0 and table_tmp[wall_i - 1][wall_j][1] == 'ǁ':
            cnt = cnt + 1
        if (wall_i - 1) >= 0 and table_tmp[wall_i - 1][wall_j][2] == '═══':
            cnt = cnt + 1
        if (wall_i - 1) >= 0 and (wall_j + 1) < info_tmp["dimensions"][1] and table_tmp[wall_i - 1][wall_j + 1][2] == '═══':
            cnt = cnt + 1
        if table_tmp[wall_i][wall_j][2] == '═══':
            cnt = cnt + 1
        if (wall_j + 1) < info_tmp["dimensions"][1] and table_tmp[wall_i][wall_j + 1][2] == '═══':
            cnt = cnt + 1
        if (wall_i + 1) < info_tmp["dimensions"][0] and table_tmp[wall_i + 1][wall_j][2] == '═══':
            cnt = cnt + 1
        if (wall_i + 1) < info_tmp["dimensions"][0] and (wall_j + 1) < info_tmp["dimensions"][1] and table_tmp[wall_i + 1][wall_j + 1][2] == '═══':
            cnt = cnt + 1
        if (wall_i + 2) < info_tmp["dimensions"][0] and table_tmp[wall_i + 2][wall_j][1] == 'ǁ':
            cnt = cnt + 1
    else:
        if (wall_j - 1) >= 0 and table_tmp[wall_i][wall_j - 1][1] == 'ǁ':
            cnt = cnt + 1
        if (wall_j - 1) >= 0 and table_tmp[wall_i][wall_j - 1][2] == '═══':
            cnt = cnt + 1
        if table_tmp[wall_i][wall_j][1] == 'ǁ':
            cnt = cnt + 1
        if table_tmp[wall_i][wall_j + 1][1] == 'ǁ':
            cnt = cnt + 1
        if (wall_j + 2) < info_tmp["dimensions"][1] and table_tmp[wall_i][wall_j + 2][2] == '═══':
            cnt = cnt + 1
        if (wall_i + 1) < info_tmp["dimensions"][0] and (wall_j - 1) >= 0 and table_tmp[wall_i + 1][wall_j - 1][1] == 'ǁ':
            cnt = cnt + 1
        if (wall_i + 1) < info_tmp["dimensions"][0] and table_tmp[wall_i + 1][wall_j][1] == 'ǁ':
            cnt = cnt + 1
        if (wall_i + 1) < info_tmp["dimensions"][0] and (wall_j + 1) < info_tmp["dimensions"][1] and table_tmp[wall_i + 1][wall_j + 1][1] == 'ǁ':
            cnt = cnt + 1
    if cnt > 1:
        return True #vraca true ako ima vise od 1 zida koji dodiruje zid (moguc zatvoren put)
    else:
        return False #vraca false ako ima 1 ili 0 zidova koji dodiruju zid (nemoguc zatvoren put)

def estimate(turn, table_tmp, info_tmp, flag):
    player_x1 = (info["player_position_x"]['x1'][0], info["player_position_x"]['x1'][1], 'x1')
    player_x2 = (info["player_position_x"]['x2'][0], info["player_position_x"]['x2'][1], 'x2')
    player_o1 = (info["player_position_o"]['o1'][0], info["player_position_o"]['o1'][1], 'o1')
    player_o2 = (info["player_position_o"]['o2'][0], info["player_position_o"]['o2'][1], 'o2')
    dest_x1 = (info["start_position_x"]['x1'][0], info["start_position_x"]['x1'][1])
    dest_x2 = (info["start_position_x"]['x2'][0], info["start_position_x"]['x2'][1])
    dest_o1 = (info["start_position_o"]['o1'][0], info["start_position_o"]['o1'][1])
    dest_o2 = (info["start_position_o"]['o2'][0], info["start_position_o"]['o2'][1])
    pathx = [0,0,0,0]
    patho = [0,0,0,0]
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'x'
    pathx[0] = len(findRoute(player_x1, dest_o1, tmp[0], tmp[1]))#put x1->o1
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'x'
    pathx[1] = len(findRoute(player_x1, dest_o2, tmp[0], tmp[1]))#put x1->o2
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'x'
    pathx[2] = len(findRoute(player_x2, dest_o1, tmp[0], tmp[1]))#put x2->o1
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'x'
    pathx[3] = len(findRoute(player_x2, dest_o2, tmp[0], tmp[1]))#put x2->o2
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'o'
    patho[0] = len(findRoute(player_o1, dest_x1, tmp[0], tmp[1]))#put o1->x1
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'o'
    patho[1] = len(findRoute(player_o1, dest_x2, tmp[0], tmp[1]))#put o1->x2
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'o'
    patho[2] = len(findRoute(player_o2, dest_x1, tmp[0], tmp[1]))#put o2->x1
    tmp = setANewState(table_tmp, info_tmp)
    tmp[1]["player_turn"] = 'o'
    patho[3] = len(findRoute(player_o2, dest_x2, tmp[0], tmp[1]))#put o2->x2

    if turn == 'x':
        if flag == 0:
            retVal = max(patho) - min(pathx) #racuna se kao najduzi put protivnika do cilja - najkraci put igraca do cilja
        elif flag == 1:
            retVal = min(pathx)
        else:
            retVal = max(patho)
    else:
        if flag == 0:
            retVal = max(pathx) - min(patho)
        elif flag == 1:
            retVal = min(patho)
        else:
            retVal = max(pathx)
    return retVal 

def getAllPossibleMoves(turn, table_tmp, info_tmp):
    if turn == "x": #Svi potezi figura x1 i x2
        figureMoves1 = getAllPossibleMovesFigure((info_tmp["player_position_x"]['x1'][0], info_tmp["player_position_x"]['x1'][1], 'x1'), table_tmp, info_tmp)
        figureMoves2 = getAllPossibleMovesFigure((info_tmp["player_position_x"]['x2'][0], info_tmp["player_position_x"]['x2'][1], 'x2'), table_tmp, info_tmp)
    else:#svi potezi figura o1 i o2
        figureMoves1 = getAllPossibleMovesFigure((info_tmp["player_position_o"]['o1'][0], info_tmp["player_position_o"]['o1'][1], 'o1'), table_tmp, info_tmp)
        figureMoves2 = getAllPossibleMovesFigure((info_tmp["player_position_o"]['o2'][0], info_tmp["player_position_o"]['o2'][1], 'o2'), table_tmp, info_tmp)
    figureMoves = figureMoves1 + figureMoves2
    retList = []
    for x in figureMoves: #svaki potez figure se prosirava sa svim mogucim kombinacijama zidova
        for i in range(info_tmp["dimensions"][0]):
            for j in range(info_tmp["dimensions"][1]):
                if (info_tmp["player_x_wall_number"][0] and turn == "x") or (info_tmp["player_o_wall_number"][0] and turn == "o"):
                     if not checkIfValidWallPosition(i, j, 1): #ako je zid moguce postaviti, vertikalni zid
                        # tmp = setANewState(table_tmp, info_tmp)
                        # if checkIfWallsAround(i, j, 1, table_tmp, info_tmp):
                        #     if checkIfClosed(tmp[0], tmp[1]):
                        retList.append((x, (i, j, 1))) #onda je ovo validan potez
                if (not info_tmp["player_x_wall_number"][0] and turn == "x") or (not info_tmp["player_o_wall_number"][0] and turn == "o"):
                    retList.append((x, ("no walls"))) #u slucaju da vise nema zidova za postaviti
                if (info_tmp["player_x_wall_number"][1] and turn == "x") or (info_tmp["player_o_wall_number"][1] and turn == "o"):
                    if not checkIfValidWallPosition(i, j, 2):#isto za horizontalni zid
                        # tmp = setANewState(table_tmp, info_tmp)
                        # if checkIfWallsAround(i, j, 2, table_tmp, info_tmp):
                        #     if checkIfClosed(tmp[0], tmp[1]):
                        retList.append((x, (i, j, 2)))
                if (not info_tmp["player_x_wall_number"][1] and turn == "x") or (not info_tmp["player_o_wall_number"][1] and turn == "o"):
                    retList.append((x, (1, 1, 1)))
    return retList



def alphaBetaMax(table_tmp, info_tmp, depth, start_d, m, turn, alpha, beta):
    tmp = setANewState(table_tmp, info_tmp)

    print("OVO JE MAX")
    drawTable(tmp[0])
    print(alpha)
    print(beta)
    
    tmp[1]["player_turn"] = turn
    lp = getAllPossibleMoves(turn, tmp[0], tmp[1])
    if depth == 0:
        return (m, estimate(turn, tmp[0], tmp[1], 0)) ##OVDE VIDI STA JE m I DA LI SE TO VRACA
    else: 
        for s in lp:
            s_tmp = setANewState(tmp[0], tmp[1])
            if s[0][2] == 'x1' or s[0][2] == 'x2':
                s_tmp[1]["player_turn"] = "x"
                if s[1] == "no walls":
                    updateTableNoWalls(s_tmp[1]["player_position_x"][s[0][2]][0], s_tmp[1]["player_position_x"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s_tmp[0], s_tmp[1])
                else:
                    updateTableWithWalls(s_tmp[1]["player_position_x"][s[0][2]][0], s_tmp[1]["player_position_x"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s[1][2], s[1][0], s[1][1], s_tmp[0], s_tmp[1])
                movePlayer(s[0][0], s[0][1], s[0][2], s_tmp[1])
            else:
                s_tmp[1]["player_turn"] = "o"
                if s[1] == "no walls":
                    updateTableNoWalls(s_tmp[1]["player_position_o"][s[0][2]][0], s_tmp[1]["player_position_o"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s_tmp[0], s_tmp[1])
                else:
                    updateTableWithWalls(s_tmp[1]["player_position_o"][s[0][2]][0], s_tmp[1]["player_position_o"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s[1][2], s[1][0], s[1][1], s_tmp[0], s_tmp[1])
                movePlayer(s[0][0], s[0][1], s[0][2], s_tmp[1])
            if turn == "x":
                turn = "o"
            else:
                turn = "x"
            alpha = max(alpha, alphaBetaMin(s_tmp[0], s_tmp[1], depth - 1, start_d, s, turn, alpha, beta), key =lambda x:x[1])
            if alpha[1] >= beta[1]:
                return beta
    return alpha

def alphaBetaMin(table_tmp, info_tmp, depth, start_d, m, turn, alpha, beta):
    tmp = setANewState(table_tmp, info_tmp)

    print("OVO JE MIN")
    drawTable(tmp[0])
    print(alpha)
    print(beta)

    tmp[1]["player_turn"] = turn
    lp = getAllPossibleMoves(turn, tmp[0], tmp[1])
    if depth == 0:
        return (m, estimate(turn, tmp[0], tmp[1], 0))
    else:
        for s in lp:
            s_tmp = setANewState(tmp[0], tmp[1])
            if s[0][2] == 'x1' or s[0][2] == 'x2':
                s_tmp[1]["player_turn"] = "x"
                if s[1] == "no walls":
                    updateTableNoWalls(s_tmp[1]["player_position_x"][s[0][2]][0], s_tmp[1]["player_position_x"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s_tmp[0], s_tmp[1])
                else:
                    updateTableWithWalls(s_tmp[1]["player_position_x"][s[0][2]][0], s_tmp[1]["player_position_x"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s[1][2], s[1][0], s[1][1], s_tmp[0], s_tmp[1])
                movePlayer(s[0][0], s[0][1], s[0][2], s_tmp[1])
            else:
                s_tmp[1]["player_turn"] = "o"
                if s[1] == "no walls":
                    updateTableNoWalls(s_tmp[1]["player_position_o"][s[0][2]][0], s_tmp[1]["player_position_o"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s_tmp[0], s_tmp[1])
                else:
                    updateTableWithWalls(s_tmp[1]["player_position_o"][s[0][2]][0], s_tmp[1]["player_position_o"][s[0][2]][1], s[0][0], s[0][1], s[0][2], s[1][2], s[1][0], s[1][1], s_tmp[0], s_tmp[1])
                movePlayer(s[0][0], s[0][1], s[0][2], s_tmp[1])
            if turn == "x":
                turn = "o"
            else:
                turn = "x"
            beta = min(beta, alphaBetaMax(s_tmp[0], s_tmp[1], depth - 1, start_d, s, turn, alpha, beta), key =lambda x:x[1])
            if beta[1] <= alpha[1]:
                return alpha
    return beta

def minimaxAlphaBeta(table_tmp, info_tmp, depth, start_d, m, turn, alpha, beta):
    if turn == 'o':
        return alphaBetaMax(table_tmp, info_tmp, depth, start_d, m, turn, alpha, beta)
    else:
        return alphaBetaMin(table_tmp, info_tmp, depth, start_d, m, turn, alpha, beta)










runGame()