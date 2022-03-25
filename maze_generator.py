import random
from PIL import Image

def drawBoard(board : list, size : int):
    imageSize = size * len(board)

    #color
    pathColor = (255, 255, 255)
    wallColor = (0, 0, 0)

    #create blank image
    image = Image.new('RGB', (imageSize, imageSize))

    #draw image
    for y in range(imageSize):
        for x in range(imageSize):
            #get i and j data to draw the right color
            i = x // size
            j = y // size

            #check if it path or wall
            color = pathColor if (board[i][j] == 0) else wallColor

            #check if it wall or start or goal
            if i == j == 1:
                color = (0, 255, 0)
            elif i == j == len(board) - 2:
                color = (255, 0, 0)
            
            #draw in current pixel
            image.putpixel((x, y), color)
    
    #save image
    image.save('maze.png')


def printBoard(board : list):
    #print board then convert all data into string
    for y in board:
        print(''.join(list(map(lambda x : '▩ ' if bool(x) else "▢ ", y))))

def normalBoard(board : list[list]):
    size = len(board)
    #insert wall at head and tail of all rows
    for i in range(size):
        board[i].insert(0, 1)
        board[i].append(1)
    #insert wall at top and bottom
    board.insert(0, [1] * (size + 2))
    board.append([1] * (size + 2))

    return board

def generateMaze(size : int):
    #create layer to draw wall
    sizeL = size * 2 - 1

    board = [[0 for i in range(sizeL)] for i in range(sizeL)]

    #list to collect rooms that can be divide
    allRooms = [((0, 0), (sizeL - 1, sizeL - 1))]

    #divide roon until there is no room to divide
    while len(allRooms) != 0:
        #choose the index 0 in first room to divide
        cRoom = allRooms[0]
        
        #get x, y length
        x = cRoom[1][0] - cRoom[0][0]
        y = cRoom[1][1] - cRoom[0][1]

        #find the longest side
        side = 1 if x >= y else 0

        #divide room half. if room is too small skip
        half = (x if bool(side) else y) // 2
        if (half < 1):
            allRooms.pop(0)
            continue
        
        #cut in y axis if (x side is longer than or equal to y) else cut in x axis
        if bool(side):
            #randomly select height to create exit
            randomMember = list(range(cRoom[0][1] // 2, cRoom[1][1] // 2 + 1))
            hole = random.choice(randomMember) * 2
            #draw wall then drill hole
            for i in range(cRoom[0][1], cRoom[1][1] + 1):
                board[i][half + cRoom[0][0]] = 1
            board[hole][half + cRoom[0][0]] = 0
            #insert data of room that is product from divide current room
            aRoom = (cRoom[0], (half + cRoom[0][0] - 1, cRoom[1][1]))
            bRoom = ((half + cRoom[0][0] + 1, cRoom[0][1]), cRoom[1])
        else:
            #randomly select length to create exit
            randomMember = list(range(cRoom[0][0] // 2, cRoom[1][0] // 2 + 1))
            hole = random.choice(randomMember) * 2
            #draw wall then drill hole
            for i in range(cRoom[0][0], cRoom[1][0] + 1):
                board[half + cRoom[0][1]][i] = 1
            board[half + cRoom[0][1]][hole] = 0
            #insert data of room that is product from divide current room
            aRoom = (cRoom[0], (cRoom[1][0], half + cRoom[0][1] - 1))
            bRoom = ((cRoom[0][0], half + cRoom[0][1] + 1), cRoom[1])

        #if aRoom and bRoom is too small don't insert their data into allRooms
        if (not (aRoom[0][0] == aRoom[1][0] or aRoom[0][1] == aRoom[1][1])):
            allRooms.append(aRoom)
        if (not (bRoom[0][0] == bRoom[1][0] or bRoom[0][1] == bRoom[1][1])):
            allRooms.append(bRoom)
        
        #remove current room data from allRooms
        allRooms.pop(0)

    #create wall all around maze
    board = normalBoard(board)

    return board

if __name__ == '__main__':
    size = 4
    imageSize = 20

    #generate maze
    board = generateMaze(pow(2, size))

    #image way (size > 7) will be weird
    drawBoard(board, imageSize)

    #text way (size > 4) will be weird
    #printBoard(board)