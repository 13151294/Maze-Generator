from ctypes import sizeof
import random
from tracemalloc import start
from PIL import Image
import time

def drawBoard(board : list, size : int):
    imageSize = size * len(board)
    pathColor = (255, 255, 255)
    wallColor = (0, 0, 0)
    image = Image.new('RGB', (imageSize, imageSize))
    print(imageSize)
    for y in range(imageSize):
        for x in range(imageSize):
            i = x // size
            j = y // size
            color = pathColor if (board[i][j] == 0) else wallColor
            if i == 1 and j == 0:
                color = (0, 255, 0)
            elif i == j == len(board) - 2:
                color = (255, 0, 0)
            image.putpixel((x, y), color)
    image.save('maze.png')


def printBoard(board : list):
    for y in board:
        print(''.join(list(map(lambda x : '▩ ' if bool(x) else "▢ ", y))))

def normalBoard(board : list[list]):
    size = len(board)
    for i in range(size):
        board[i].insert(0, 1)
        board[i].append(1)
    board.insert(0, [1] * (size + 2))
    board.append([1] * (size + 2))

    return board

def generateMaze(size : int):
    start = time.time()
    sizeL = size * 2 - 1
    board = [[0 for i in range(sizeL)] for i in range(sizeL)]
    done = False

    allRooms = [((0, 0), (sizeL - 1, sizeL - 1))]
    closeRooms = []

    count = 0
    while len(allRooms) != 0:
        count += 1
        #print attemps
        print('-' * 20)
        print(f'attemps : {count}')
        #current allRooms
        cRoom = allRooms[0]
        x = cRoom[1][0] - cRoom[0][0]
        y = cRoom[1][1] - cRoom[0][1]
        #find the longest side
        side = 1 if x >= y else 0
        #divide room half then make exit
        half = (x if bool(side) else y) // 2
        if (half < 1):
            continue
        
        if bool(side):
            randomMember = list(range(cRoom[0][1] // 2, cRoom[1][1] // 2 + 1))
            hole = random.choice(randomMember) * 2
            for i in range(cRoom[0][1], cRoom[1][1] + 1):
                board[i][half + cRoom[0][0]] = 1
            board[hole][half + cRoom[0][0]] = 0
            aRoom = (cRoom[0], (half + cRoom[0][0] - 1, cRoom[1][1]))
            bRoom = ((half + cRoom[0][0] + 1, cRoom[0][1]), cRoom[1])
        else:
            randomMember = list(range(cRoom[0][0] // 2, cRoom[1][0] // 2 + 1))
            hole = random.choice(randomMember) * 2
            for i in range(cRoom[0][0], cRoom[1][0] + 1):
                board[half + cRoom[0][1]][i] = 1
            board[half + cRoom[0][1]][hole] = 0
            aRoom = (cRoom[0], (cRoom[1][0], half + cRoom[0][1] - 1))
            bRoom = ((cRoom[0][0], half + cRoom[0][1] + 1), cRoom[1])

        if (not (aRoom[0][0] == aRoom[1][0] or aRoom[0][1] == aRoom[1][1])):
            allRooms.extend([aRoom, bRoom])

        closeRooms.append(allRooms.pop(0))

    print('-' * 20)
    

    print(f'time use : {(time.time() - start) * 1000}')

    board = normalBoard(board)

    return board

if __name__ == '__main__':
    start = time.time()
    board = generateMaze(512)
    print((time.time() - start) * 1000)

    drawBoard(board, 20)