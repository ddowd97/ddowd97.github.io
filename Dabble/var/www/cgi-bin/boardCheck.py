#!/usr/bin/python
# Python Interpreter is 3.8.2, ran through PyCharm 2019.3.3

# Name:             David Dowd
# ECN Login:        ddowd

from PIL import Image, ImageDraw, ImageFont
from operator import itemgetter
import sys
import time
import cgi, cgitb
import operator
from collections import deque
from operator import eq

form = cgi.FieldStorage()

wordDictionary = {}

with open('chosenDict.txt', "r") as chosenDict:
    chosenDictName = chosenDict.readline()

with open(chosenDictName, "r") as scrabbleDictionary:
    for line in scrabbleDictionary:
        line = line.replace('\t', ' ')
        wordDictionary[line.split(' ', 1)[0]] = line.split(' ', 1)[1]

letterList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letterPointDict = { "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3,
                    "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
}

previousBoard = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                 ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

oldBoard = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

newBoard = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

resetBoard = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '-', '-', '-', '-', '-', '-', '-', '-', '-', '#'],
              ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

emptyBoard = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
              ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

scratchBoard = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

board1 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', 's', ' ', 's', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', 'n', ' ', 'm', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', 'a', ' ', 'i', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', 'k', 'i', 't', 'e', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', 'e', ' ', 'e', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

board2 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', 'a', 't', 't', 'a', 'c', 'k', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', 'r', ' ', 'a', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', 'a', ' ', 'r', ' ', ' ', ' ', 't', '#'],
          ['#', ' ', 'i', 's', 'm', ' ', 'r', 'o', 'b', 'e', '#'],
          ['#', ' ', ' ', 'h', 'u', 'm', 'a', 'n', ' ', 'l', '#'],
          ['#', ' ', ' ', ' ', 's', ' ', 'k', ' ', ' ', 'l', '#'],
          ['#', ' ', ' ', 'n', 'e', 'v', 'e', 'r', ' ', 'e', '#'],
          ['#', ' ', 'r', 'o', 't', ' ', ' ', ' ', ' ', 'r', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

board3 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', 't', 'e', 's', 'l', 'a', ' ', 'p', '#'],
          ['#', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', 'e', '#'],
          ['#', ' ', ' ', 'r', 'a', 'c', 'q', 'u', 'e', 't', '#'],
          ['#', ' ', ' ', 'q', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', ' ', ' ', 'u', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

counter = 0
with open('currentBoard.txt', 'r') as boardFile:
    line = boardFile.readline()
    for char in line:
        if char == '0':
            oldBoard[int((counter / 9)) + 1][int((counter % 9)) + 1] = ' '
        else:
            oldBoard[int((counter / 9)) + 1][int((counter % 9)) + 1] = char
        counter += 1

counter = 0
with open('previousBoard.txt', 'r') as boardFile:
    line = boardFile.readline()
    for char in line:
        if char == '0':
            previousBoard[int((counter / 9)) + 1][int((counter % 9)) + 1] = ' '
        else:
            previousBoard[int((counter / 9)) + 1][int((counter % 9)) + 1] = char
        counter += 1

def checkNeighbors(board, counterY, counterX):
    up, down, left, right = -1, - 1, -1, -1
    if board[counterY-1][counterX] != '#':
        if board[counterY-1][counterX] != ' ':
            up = 1
        else:
            up = 0
    if board[counterY+1][counterX] != '#':
        if board[counterY+1][counterX] != ' ':
            down = 1
        else:
            down = 0
    if board[counterY][counterX-1] != '#':
        if board[counterY][counterX-1] != ' ':
            left = 1
        else:
            left = 0
    if board[counterY][counterX+1] != '#':
        if board[counterY][counterX+1] != ' ':
            right = 1
        else:
            right = 0

    return up, down, left, right


def checkBoard(originalBoard, newBoard):
    y = 0
    x = 0
    localCounter = 0
    letterCounter = 0
    locList = []
    neighbors = (-1, 0), (0, +1), (+1, 0), (0, -1)
    similar = eq

    for row in newBoard:
        x = 0
        for col in row:
            if (newBoard[y][x] != originalBoard[y][x]): # If a new letter has been placed, continue
                if (originalBoard[y][x] != ' '): # If this new letter has been placed over what previously was NOT a blank space, return 0 (INVALID)
                    return 0
                scratchBoard[y][x] = '!'
                scratchNeighborTuple = checkNeighbors(scratchBoard, y, x)
                neighborTuple = checkNeighbors(newBoard, y, x)
                newNeighborTuple = checkNeighbors(originalBoard, y, x)
                if 1 in neighborTuple:  # If this space has a neighbor tile
                    diffTuple = tuple(map(operator.sub, neighborTuple, newNeighborTuple))
                    if diffTuple.count(1) > 2: # New tile can have no more than 2 other neighbors that are also new tiles
                        return 0
                    elif diffTuple.count(1) == 2: # If a tile has 2 neighbors that are also new, they must be in same line
                        if (diffTuple[0] == 1 or diffTuple[1] == 1) and (diffTuple[2] == 1 or diffTuple[3] == 1):
                            return 0
                    separateFlag = 1
                    hitFlag = 0
                    upCounter = 0
                    downCounter = 0
                    leftCounter = 0
                    rightCounter = 0
                    if (originalBoard[y - 1][x] != ' ' and originalBoard[y - 1][x] != '#') or (originalBoard[y + 1][x] != ' ' and originalBoard[y + 1][x] != '#') or (originalBoard[y][x - 1] != ' ' and originalBoard[y][x - 1] != '#') or (originalBoard[y][x + 1] != ' ' and originalBoard[y][x + 1] != '#'):
                        hitFlag = 1
                        separateFlag = 0
                    if neighborTuple[0] == 1 and neighborTuple[1] == 1:  # There are checkable tiles vertically upwards and downwards
                        tempUpY = y - 1
                        tempDownY = y + 1
                        upCounter = 1
                        downCounter = 1
                        while checkNeighbors(newBoard, tempUpY, x)[0] == 1:
                            if hitFlag == 0:
                                if (originalBoard[tempUpY - 1][x] != ' ' and originalBoard[tempUpY - 1][x] != '#') or (originalBoard[tempUpY][x - 1] != ' ' and originalBoard[tempUpY][x - 1] != '#') or (originalBoard[tempUpY][x + 1] != ' ' and originalBoard[tempUpY][x + 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            upCounter += 1
                            tempUpY -= 1
                        while checkNeighbors(newBoard, tempDownY, x)[1] == 1:
                            if hitFlag == 0:
                                if (originalBoard[tempDownY + 1][x] != ' ' and originalBoard[tempDownY + 1][x] != '#') or (originalBoard[tempDownY][x - 1] != ' ' and originalBoard[tempDownY][x - 1] != '#') or (originalBoard[tempDownY][x + 1] != ' ' and originalBoard[tempDownY][x + 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            downCounter += 1
                            tempDownY += 1
                        temp = ''
                        for letter in range(tempUpY, tempDownY+1):
                            temp = temp + newBoard[letter][x]
                        if temp.upper() not in wordDictionary:
                            return 0
                    elif neighborTuple[0] == 1:  # There are checkable tiles vertically upwards, not downwards
                        separateFlag = 0
                        tempUpY = y - 1
                        upCounter = 1
                        while checkNeighbors(newBoard, tempUpY, x)[0] == 1:
                            if hitFlag == 0:
                                if (originalBoard[tempUpY - 1][x] != ' ' and originalBoard[tempUpY - 1][x] != '#') or (originalBoard[tempUpY][x - 1] != ' ' and originalBoard[tempUpY][x - 1] != '#') or (originalBoard[tempUpY][x + 1] != ' ' and originalBoard[tempUpY][x + 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            upCounter += 1
                            tempUpY -= 1
                        temp = ''
                        for letter in range(tempUpY, y+1):
                            temp = temp + newBoard[letter][x]
                        if temp.upper() not in wordDictionary:
                            return 0
                    elif neighborTuple[1] == 1:  # There are checkable tiles vertically downwards, not upwards
                        separateFlag = 0
                        tempDownY = y + 1
                        downCounter = 1
                        while checkNeighbors(newBoard, tempDownY, x)[1] == 1:
                            if hitFlag == 0:
                                if (originalBoard[tempDownY + 1][x] != ' ' and originalBoard[tempDownY + 1][x] != '#') or (originalBoard[tempDownY][x - 1] != ' ' and originalBoard[tempDownY][x - 1] != '#') or (originalBoard[tempDownY][x + 1] != ' ' and originalBoard[tempDownY][x + 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            downCounter += 1
                            tempDownY += 1
                        temp = ''
                        for letter in range(y, tempDownY+1):
                            temp = temp + newBoard[letter][x]
                        if temp.upper() not in wordDictionary:
                            return 0
                    if neighborTuple[2] == 1 and neighborTuple[3] == 1:  # There are checkable tiles horizontally to the left and to the right
                        separateFlag = 0
                        tempLeftX = x - 1
                        tempRightX = x + 1
                        leftCounter = 1
                        rightCounter = 1
                        while checkNeighbors(newBoard, y, tempLeftX)[2] == 1:
                            if hitFlag == 0:
                                if (originalBoard[y - 1][tempLeftX] != ' ' and originalBoard[y - 1][tempLeftX] != '#') or (originalBoard[y + 1][tempLeftX] != ' ' and originalBoard[y + 1][tempLeftX] != '#') or (originalBoard[y][tempLeftX - 1] != ' ' and originalBoard[y][tempLeftX - 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            leftCounter += 1
                            tempLeftX -= 1
                        while checkNeighbors(newBoard, y, tempRightX)[3] == 1:
                            if hitFlag == 0:
                                if (originalBoard[y - 1][tempRightX] != ' ' and originalBoard[y - 1][tempRightX] != '#') or (originalBoard[y + 1][tempRightX] != ' ' and originalBoard[y + 1][tempRightX] != '#') or (originalBoard[y][tempRightX + 1] != ' ' and originalBoard[y][tempRightX + 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            rightCounter += 1
                            tempRightX += 1
                        temp = ''
                        for letter in range(tempLeftX, tempRightX+1):
                            temp = temp + newBoard[y][letter]
                        if temp.upper() not in wordDictionary:
                            return 0
                    elif neighborTuple[2] == 1:  # There are checkable tiles horizontally to the left, not to the right
                        tempLeftX = x - 1
                        leftCounter = 1
                        while checkNeighbors(newBoard, y, tempLeftX)[2] == 1:
                            if hitFlag == 0:
                                if (originalBoard[y - 1][tempLeftX] != ' ' and originalBoard[y - 1][tempLeftX] != '#') or (originalBoard[y + 1][tempLeftX] != ' ' and originalBoard[y + 1][tempLeftX] != '#') or (originalBoard[y][tempLeftX - 1] != ' ' and originalBoard[y][tempLeftX - 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            leftCounter += 1
                            tempLeftX -= 1
                        temp = ''
                        for letter in range(tempLeftX, x+1):
                            temp = temp + newBoard[y][letter]
                        if temp.upper() not in wordDictionary:
                            return 0
                    elif neighborTuple[3] == 1:  # There are checkable tiles horizontally to the right, not to the left
                        tempRightX = x + 1
                        rightCounter = 1
                        while checkNeighbors(newBoard, y, tempRightX)[3] == 1:
                            if hitFlag == 0:
                                if (originalBoard[y - 1][tempRightX] != ' ' and originalBoard[y - 1][tempRightX] != '#') or (originalBoard[y + 1][tempRightX] != ' ' and originalBoard[y + 1][tempRightX] != '#') or (originalBoard[y][tempRightX + 1] != ' ' and originalBoard[y][tempRightX + 1] != '#'):
                                    hitFlag = 1
                                    separateFlag = 0
                            rightCounter += 1
                            tempRightX += 1
                        temp = ''
                        for letter in range(x, tempRightX+1):
                            temp = temp + newBoard[y][letter]
                        if temp.upper() not in wordDictionary:
                            return 0
                    if separateFlag == 1: # If a new word is separated from the rest of the board (may have neighbors, but they are new too)
                        # AND if the old board WASN'T empty (first turn checker)
                        if originalBoard != emptyBoard:
                            return 0
                        # AND if the middle tile IS empty (first turn checker)
                        elif newBoard[5][5] == ' ':
                            return 0
                        # AND if any diagonal adjacent to the middle is occupied (first turn checker)
                        elif (newBoard[4][4] != ' ') or (newBoard[4][6] != ' ') or (newBoard[6][4] != ' ') or (newBoard[6][6] != ' '):
                            return 0
                    localCounter += 1
                    locList.append((y, x))
                else:
                    return 0
            x += 1
        y += 1

    if len(locList) > 0:
        i = 1
        while i < len(locList): # For every distinct location
            if locList[0][0] != locList[i][0] and locList[0][1] != locList[i][1]: # If both X and Y differed from that of the first placed tile, exit
                return 0
            i += 1

    return 1

flag = -1
'''
boardVal = int(form.getvalue('board'))

if boardVal == 1 or boardVal == 2 or boardVal == 3:
    if boardVal == 1:
        board = board1
    elif boardVal == 2:
        board = board2
    else:
        board = board3
    if checkBoard(emptyBoard, board) == 1:
        flag = 1
    else:
        flag = 0
else:
'''
new_counter = 0
boardState = str(form.getvalue('board'))
if len(boardState) == 1:
    if checkBoard(previousBoard, oldBoard) == 1:
        flag = 1
    else:
        flag = 0
else:
    for char in boardState:
        if char == '0':
            newBoard[int((new_counter / 9)) + 1][int((new_counter % 9)) + 1] = ' '
        else:
            newBoard[int((new_counter / 9)) + 1][int((new_counter % 9)) + 1] = char
        new_counter += 1
    if newBoard == resetBoard: # If we are sent 81 - characters, reset the board and output 1
        flag = 1
        previousBoard = emptyBoard
        oldBoard = emptyBoard
        with open('currentBoard.txt', 'w') as currFile:
            for line in emptyBoard:
                for char in line:
                    if char != '#':
                        currFile.write('0')
        with open('previousBoard.txt', 'w') as prevFile:
            for line in emptyBoard:
                for char in line:
                    if char != '#':
                        prevFile.write('0')
    elif checkBoard(oldBoard, newBoard) == 1: # Else if we are sent an attempt at a real board, check and return
        flag = 1
        previousBoard = oldBoard
        oldBoard = newBoard
        with open('currentBoard.txt', 'w') as boardFile:
            for line in oldBoard:
                for char in line:
                    if char != '#':
                        if char == ' ':
                            boardFile.write('0')
                        else:
                            boardFile.write(char)
        with open('previousBoard.txt', 'w') as prevFile:
            for line in previousBoard:
                for char in line:
                    if char != '#':
                        if char == ' ':
                            prevFile.write('0')
                        else:
                            prevFile.write(char)
    else:
        flag = 0

if flag == 1:
    img = Image.new('RGB', (280, 280), color=(255, 255, 255))
    
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("arial.ttf", 20)

    # Horizontal Dividers
    d.line((0, 35, 300, 35), fill=0)
    d.line((0, 65, 300, 65), fill=0)
    d.line((0, 95, 300, 95), fill=0)
    d.line((0, 125, 300, 125), fill=0)
    d.line((0, 155, 300, 155), fill=0)
    d.line((0, 185, 300, 185), fill=0)
    d.line((0, 215, 300, 215), fill=0)
    d.line((0, 245, 300, 245), fill=0)

    # Vertical Dividers
    d.line((35, 0, 35, 300), fill=0)
    d.line((65, 0, 65, 300), fill=0)
    d.line((95, 0, 95, 300), fill=0)
    d.line((125, 0, 125, 300), fill=0)
    d.line((155, 0, 155, 300), fill=0)
    d.line((185, 0, 185, 300), fill=0)
    d.line((215, 0, 215, 300), fill=0)
    d.line((245, 0, 245, 300), fill=0)

    # Fix square colors
    d.rectangle((0, 0, 0, 279), fill=(255, 255, 255), outline=0)
    d.rectangle((0, 0, 279, 0), fill=(255, 255, 255), outline=0)
    d.rectangle((279, 0, 279, 279), fill=(255, 255, 255), outline=0)
    d.rectangle((0, 279, 279, 279), fill=(255, 255, 255), outline=0)
    d.rectangle((125, 125, 155, 155), fill=(180, 180, 180), outline=0)
    # 3W
    d.rectangle((0, 0, 35, 35), fill=255, outline=0)
    d.rectangle((245, 0, 279, 35), fill=255, outline=0)
    d.rectangle((0, 245, 35, 279), fill=255, outline=0)
    d.rectangle((245, 245, 279, 279), fill=255, outline=0)
    # 2W
    d.rectangle((35, 35, 65, 65), fill=(255, 105, 180), outline=0)
    d.rectangle((215, 35, 245, 65), fill=(255, 105, 180), outline=0)
    d.rectangle((35, 215, 65, 245), fill=(255, 105, 180), outline=0)
    d.rectangle((215, 215, 245, 245), fill=(255, 105, 180), outline=0)
    # 3L
    d.rectangle((65, 65, 95, 95), fill=(27, 103, 179), outline=0)
    d.rectangle((185, 65, 215, 95), fill=(27, 103, 179), outline=0)
    d.rectangle((65, 185, 95, 215), fill=(27, 103, 179), outline=0)
    d.rectangle((185, 185, 215, 215), fill=(27, 103, 179), outline=0)
    # 2L
    d.rectangle((95, 95, 125, 125), fill=(102, 255, 255), outline=0)
    d.rectangle((155, 95, 185, 125), fill=(102, 255, 255), outline=0)
    d.rectangle((95, 155, 125, 185), fill=(102, 255, 255), outline=0)
    d.rectangle((155, 155, 185, 185), fill=(102, 255, 255), outline=0)
    d.rectangle((125, 0, 155, 35), fill=(102, 255, 255), outline=0)
    d.rectangle((125, 245, 155, 279), fill=(102, 255, 255), outline=0)
    d.rectangle((0, 125, 35, 155), fill=(102, 255, 255), outline=0)
    d.rectangle((245, 125, 279, 155), fill=(102, 255, 255), outline=0)

    counter = 0
    with open('currentBoard.txt', 'r') as boardFile:
        line = boardFile.readline()
        for char in line:
            if char == '0':
                d.text((15 + 30 * (counter % 9), 10 + 30 * int(counter / 9)), " ", font=fnt, fill=(0, 0, 0))
            else:
                d.text((15 + 30 * (counter % 9), 10 + 30 * int(counter / 9)), char, font=fnt, fill=(0, 0, 0))
            counter += 1

    img.save('boardImage.png')



#form = cgi.FieldStorage()
#temp = form.getvalue('temp')
print("Content-type:text/html\r\n\r\n")
print('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
print('<html>')
print('<html xmlns="http://www.w3.org/1999/xhtml">')
print('<head>')

print('<style>')
print('.center {')
print(' display: block;')
print(' margin-left: auto;')
print(' margin-right: auto;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/howto/howto_js_accordion.asp
print('.accordion {')
print('  background-color: #eee;')
print('  color: #444;')
print('  cursor: pointer;')
print('  padding: 18px;')
print('  width: 100%;')
print('  text-align: left;')
print('  border: none;')
print('  outline: none;')
print('  transition: 0.4s;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/howto/howto_js_accordion.asp
print('.active, .accordion:hover {')
print('  background-color: #ccc;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/howto/howto_js_accordion.asp
print('.panel {')
print('  padding: 0 18px;')
print('  background-color: white;')
print('  display: none;')
print('  overflow: hidden;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/html/html_tables.asp
print('table {')
print('  font-family: arial, sans-serif;')
print('  border-collapse: collapse;')
print('  width: 100%;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/html/html_tables.asp
print('td, th {')
print('  border: 1px solid #cccccc;')
print('  text-align: left;')
print('  padding: 8px;')
print('}')
# CSS Sample from Source: https://www.w3schools.com/html/html_tables.asp
print('tr:nth-child(even) {')
print('  background-color: #eeeeee;')
print('}')
print('</style>')

print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
print('<base href="https://engineering.purdue.edu/477grp15/" />')
print('<title>Board Checked!</title>')
print('<meta name="keywords" content="" />')
print('<meta name="description" content="" />')
print('<meta name="author" content="George Hadley">')
print('<meta name = "format-detection" content = "telephone=no" />')
print('<meta name="viewport" content="width=device-width,initial-scale=1.0">')
print('<link rel="stylesheet" href="css/default.css" type="text/css" media="all" />')
print('<link rel="stylesheet" href="css/responsive.css">')
print('<link rel="stylesheet" href="css/styles_new.css">')
print('<link rel="stylesheet" href="css/content.css">')
print('</head>')



print('<body>')
print('<div id="wrapper_site">')
print('    <div id="wrapper_page">')
print('    <div id="header"></div>')
print('    <div id="menu"></div>')
print('    <div id="banner">')
print('        <img src="Team/img/BannerImgExample.jpg"></img>')
print('    </div>')
print('    <div id="content">')
print('        <button class="accordion">Rules of Dabble</button>')
print('        <div class="panel">')
print('          <p>1) Players take turns placing one word at a time on the Dabble board.<br>')
print('             2) Players may pass their turn, if they so choose.<br>')
print('             3) Words placed on the board must be defined in the current dictionary.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Placed words must not, as a consequence, form other words that are not defined in the current dictionary.<br>')
print('             4) The first word placed must use the center of the board.<br>')
print('             5) Words placed on the board must be connected to all other previously placed words.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) Placed words must either EXTEND, HOOK, or be PARALLEL to previous words.<br>')
print('             6) The game ends when the score limit [if specified] is reached or when six consecutive passes occur.')
print('          </p>')
print('    </div>')
print('        <button class="accordion">Scoring System</button>')
print('        <div class="panel">')
print('          <p>1) A bonus space (<b>DL</b>, <b>TL</b>, <b>DW</b>, <b>TW</b>) is only used one time - when a new letter is placed on it.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a) <b>DL</b> = Double Letter, <b>TL</b> = Triple Letter, <b>DW</b> = Double Word, <b>TW</b> = Triple Word<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) The center of the board is a <b>DW</b> bonus space.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b) Letter bonuses are applied before word bonuses - word bonuses come last!<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c) Word bonuses are applied to all words directly formed by that placed tile.<br>')
print('             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) Word bonuses are stackable - 2 <b>DW</b> ("Double-Double") is a x4 bonus, 2 <b>TW</b> ("Triple-Triple") is a x9 bonus!<br>')
print('             2) Using all 7 tiles in one turn is a BINGO and awards 50 extra points (after bonus space calculation)!<br>')
print('             3) No points are deducted when passing a turn.')
print('          </p>')
print('    </div>')
print('        <button class="accordion">Letter Point Distribution</button>')
print('        <div class="panel">')
print('          <p><table>')
print('              <tr><th>Letter</th><th>Points</th></tr>')
print('              <tr><td>A</td><td>1</td></tr>')
print('              <tr><td>B</td><td>3</td></tr>')
print('              <tr><td>C</td><td>3</td></tr>')
print('              <tr><td>D</td><td>2</td></tr>')
print('              <tr><td>E</td><td>1</td></tr>')
print('              <tr><td>F</td><td>4</td></tr>')
print('              <tr><td>G</td><td>2</td></tr>')
print('              <tr><td>H</td><td>4</td></tr>')
print('              <tr><td>I</td><td>1</td></tr>')
print('              <tr><td>J</td><td>8</td></tr>')
print('              <tr><td>K</td><td>5</td></tr>')
print('              <tr><td>L</td><td>1</td></tr>')
print('              <tr><td>M</td><td>3</td></tr>')
print('              <tr><td>N</td><td>1</td></tr>')
print('              <tr><td>O</td><td>1</td></tr>')
print('              <tr><td>P</td><td>3</td></tr>')
print('              <tr><td>Q</td><td>10</td></tr>')
print('              <tr><td>R</td><td>1</td></tr>')
print('              <tr><td>S</td><td>1</td></tr>')
print('              <tr><td>T</td><td>1</td></tr>')
print('              <tr><td>U</td><td>1</td></tr>')
print('              <tr><td>V</td><td>4</td></tr>')
print('              <tr><td>W</td><td>4</td></tr>')
print('              <tr><td>X</td><td>8</td></tr>')
print('              <tr><td>Y</td><td>4</td></tr>')
print('              <tr><td>Z</td><td>10</td></tr>')
print('             </table>')
print('          </p>')
print('        </div>')
# The following <script> is borrowed from the source https://www.w3schools.com/howto/howto_js_accordion.asp
print('        <script>')
print('        var acc = document.getElementsByClassName("accordion");')
print('        var i;')

print('        for (i = 0; i < acc.length; i++) {')
print('          acc[i].addEventListener("click", function() {')
print('            this.classList.toggle("active");')
print('            var panel = this.nextElementSibling;')
print('            if (panel.style.display === "block") {')
print('              panel.style.display = "none";')
print('            } else {')
print('              panel.style.display = "block";')
print('            }')
print('          });')
print('        }')
print('        </script>')
print('        <br><br>')
print('        <FORM action="var/www/cgi-bin/loadDabble.py" method="get">')
print('            <INPUT TYPE="Submit" Value="REFRESH">')
print('        </FORM>')
print('        <h2>Dabble Dictionary Support</h2>')
print('        <FORM action="var/www/cgi-bin/chooseDict.py" method="get">')
if chosenDictName == 'CollinsDictionary.txt':
  print('            Collins Dictionary<input type="radio" name="dict" value="1" checked> Chosen!<br>')
  print('            Oxford English Dictionary<input type="radio" name="dict" value="2"><br>')
  print('            Word Dump <i>(<b>Experimental</b> - Some Undefined/Obscure Words, Longer Processing Time)</i><input type="radio" name="dict" value="3"><br>')
elif chosenDictName == 'OxfordEnglishDictionary.txt':
  print('            Collins Dictionary<input type="radio" name="dict" value="1"><br>')
  print('            Oxford English Dictionary<input type="radio" name="dict" value="2" checked> Chosen!<br>')
  print('            Word Dump <i>(<b>Experimental</b> - Some Undefined/Obscure Words, Longer Processing Time)</i><input type="radio" name="dict" value="3"><br>')
else:
  print('            Collins Dictionary<input type="radio" name="dict" value="1"><br>')
  print('            Oxford English Dictionary<input type="radio" name="dict" value="2"><br>')
  print('            Word Dump <i>(<b>Experimental</b> - Some Undefined/Obscure Words, Longer Processing Time)</i><input type="radio" name="dict" value="3" checked> Chosen!<br>')
print('            <INPUT TYPE="Submit" Value="Choose my dictionary!">')
print('        </FORM>')
print('        <br>')
print('        <h2>Dabble Word Checker</h2>')
print('        <FORM action="var/www/cgi-bin/wordCheck.py" method="get">')
print('            Please enter your word (e.g. "pencil"):<br>')
print('            <INPUT TYPE="Text" Size="3" maxlength="7" name="temp">&nbsp;<INPUT TYPE="Submit" Value="Check my word!">')
print('        </FORM>')
print('        <br>')
print('        <h2>Dabble Word Recommender</h2>')
print('        <FORM action="var/www/cgi-bin/permuteCheck.py" method="get">')
if chosenDictName == 'CollinsDictionary.txt':
    print("            Please enter your 7 letters (e.g. 'abcdefg'). Keep in mind that the current dictionary in play is Collin's Dictionary.<br>")
elif chosenDictName == 'OxfordEnglishDictionary.txt':
    print("            Please enter your 7 letters (e.g. 'abcdefg'). Keep in mind that the current dictionary in play is the Oxford English Dictionary.<br>")
else:
    print("            Please enter your 7 letters (e.g. 'abcdefg'). Keep in mind that the current dictionary in play is the Word Dump.<br>")
print('            <INPUT TYPE="Text" Size="3" maxlength="7" name="temp">&nbsp;<INPUT TYPE="Submit" Value="Recommend me a word!">')
print('        </FORM><br>')
print('        <h2>Dabble Board Verifier</h2>')
print('        <FORM action="var/www/cgi-bin/boardCheck.py" method="get">')
'''
print('            <img src="Team/progress/img/board1.png" width=281 height=142>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
print('            <img src="Team/progress/img/board2.png" width=281 height=142>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
print('            <img src="Team/progress/img/board3.png" width=281 height=142><br>')
if boardVal == 1:
    print('            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Board1<input type="radio" name="board" value="1" checked>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
else:
    print('            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Board1<input type="radio" name="board" value="1">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
if boardVal == 2:
    print('            &emsp;&emsp;Board2<input type="radio" name="board" value="2" checked>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
else:
    print('            &emsp;&emsp;Board2<input type="radio" name="board" value="2">&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;')
if boardVal == 3:
    print('            Board3<input type="radio" name="board" value="3" checked><br><br>')
else:
    print('            Board3<input type="radio" name="board" value="3"><br><br>')
'''

print('            <img src="var/www/cgi-bin/boardImage.png" width=280 height=280 class="center"><br>')
print('            <p style="text-align:center">Current Board<input type="radio" name="board" value="1" checked></p><br>')
print('            <p style="text-align:center">(Enter <b>CTRL + F5</b> if the image does not refresh on your screen.)')
print('            <p style="text-align:center"><INPUT TYPE="Submit" Value="Check my board!">')
print('            <br>')
if flag == 1:
    print('            This board is valid!<br>')
elif flag == 0:
    print("            This board isn't valid!<br>")
print('        </FORM>')
print('    </div>')
print('    <div id="footer"></div>')
print('    </div>')
print('</div>')

print('<script src="js/jquery.js"></script>')
print('<script src="js/jquery-migrate-1.1.1.js"></script>')
print('<script type="text/javascript">')
print('$(document).ready(function() {')
print('    $("#header").load("header.html");')
print('    $("#menu").load("navbar_new.html");')
print('    $("#member1").load("Team/czatloko.html");')
print('    $("#member2").load("Team/delagarm.html");')
print('    $("#member3").load("Team/wilso822.html");')
print('    $("#member4").load("Team/ddowd.html");')
print('    $("#footer").load("footer.html");')
print('});')
print('</script>')
print('</body>')
print('</html>')