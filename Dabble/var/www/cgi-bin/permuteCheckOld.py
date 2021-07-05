#!/usr/bin/env python
# Python Interpreter is 3.8.1, ran through PyCharm 2019.3.3

# Name:             David Dowd
# ECN Login:        ddowd

from operator import itemgetter
import sys
import time
import cgi, cgitb

form = cgi.FieldStorage()

wordDictionary = {}
# Collins Scrabble Words: A word list used in English-language tournament Scrabble in most countries.
with open('ScrabbleDictionary.txt', "r") as scrabbleDictionary:
    for line in scrabbleDictionary:
        line = line.replace('\t', ' ')
        wordDictionary[line.split(' ', 1)[0]] = line.split(' ', 1)[1]

letterList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letterPointDict = { "a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3,
                    "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10
}
wordScoreArray = [[3, 1, 1, 1, 1, 1, 1, 1, 3],
                  [1, 2, 1, 1, 1, 1, 1, 2, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 2, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 2, 1, 1, 1, 1, 1, 2, 1],
                  [3, 1, 1, 1, 1, 1, 1, 1, 3]]

letterScoreArray = [[1, 1, 1, 1, 2, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 3, 1, 1, 1, 3, 1, 1],
                    [1, 1, 1, 2, 1, 2, 1, 1, 1],
                    [2, 1, 1, 1, 1, 1, 1, 1, 2],
                    [1, 1, 1, 2, 1, 2, 1, 1, 1],
                    [1, 1, 3, 1, 1, 1, 3, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 2, 1, 1, 1, 1]]

boardArray = [['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
              ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''],
              ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', '', '']]

emptyBoard= [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
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

sampleBoardArray1 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                     ['#', 'a', 't', 't', 'a', 'c', 'k', ' ', ' ', ' ', '#'],
                     ['#', ' ', ' ', 'r', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                     ['#', ' ', ' ', 'a', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                     ['#', ' ', ' ', 's', ' ', ' ', 'r', ' ', ' ', ' ', '#'],
                     ['#', ' ', ' ', 'h', 'u', 'm', 'a', 'n', ' ', ' ', '#'],
                     ['#', ' ', ' ', ' ', 's', ' ', 'k', ' ', ' ', ' ', '#'],
                     ['#', ' ', ' ', 'n', 'e', 'v', 'e', 'r', ' ', ' ', '#'],
                     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

sampleBoardArray1_2 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
                       ['#', 'a', 't', 't', 'a', 'c', 'k', ' ', ' ', ' ', '#'],
                       ['#', ' ', ' ', 'r', ' ', 'a', ' ', ' ', ' ', ' ', '#'],
                       ['#', ' ', ' ', 'a', ' ', 'r', ' ', ' ', ' ', ' ', '#'],
                       ['#', ' ', ' ', 's', ' ', 'o', 'r', ' ', ' ', ' ', '#'],
                       ['#', ' ', ' ', 'h', 'u', 'm', 'a', 'n', ' ', ' ', '#'],
                       ['#', ' ', ' ', ' ', 's', ' ', 'k', ' ', ' ', ' ', '#'],
                       ['#', ' ', ' ', 'n', 'e', 'v', 'e', 'r', ' ', ' ', '#'],
                       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
                       ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

sampleBoardArray1Mod = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
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

sampleBoardArray2 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
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

# Modified implementation of the Steinhaus-Johnson-Trotter algorithm by rosettacode.org
# Original source: https://rosettacode.org/wiki/Permutations_by_swapping#Python
def permutation(n):
    sign = 1
    p = [[i, 0 if i == 0 else -1]
         for i in range(n)]

    yield tuple(pp[0] for pp in p), sign

    while any(pp[1] for pp in p):
        i1, (n1, d1) = max(((i, pp) for i, pp in enumerate(p) if pp[1]), key=itemgetter(1))
        sign *= -1
        if d1 == -1:
            i2 = i1 - 1
            p[i1], p[i2] = p[i2], p[i1]
            if i2 == 0 or p[i2 - 1][0] > n1:
                p[i2][1] = 0
        elif d1 == 1:
            i2 = i1 + 1
            p[i1], p[i2] = p[i2], p[i1]
            if i2 == n - 1 or p[i2 + 1][0] > n1:
                p[i2][1] = 0
        yield tuple(pp[0] for pp in p), sign

        for i3, pp in enumerate(p):
            n3, d3 = pp
            if n3 > n1:
                pp[1] = 1 if i3 < i2 else -1


# Value of -1: Outside of board
# Value of  0: Empty space
# Value of  1: Neighboring character
def checkNeighbors(board: list, counterY: int, counterX: int):
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

def checkBoard(originalBoard: list, newBoard: list) -> bool:
    y = 0
    x = 0
    for row in newBoard:
        x = 0
        for col in row:
            if newBoard[y][x] != originalBoard[y][x]:
                print("x:", y, "y:", x, "is different.. letter is", newBoard[y][x])
                neighborTuple = checkNeighbors(newBoard, y, x)
                print(neighborTuple)
                if 1 in neighborTuple:  # If this space has a neighbor tile
                    upCounter = 0
                    downCounter = 0
                    leftCounter = 0
                    rightCounter = 0
                    if neighborTuple[0] == 1 and neighborTuple[1] == 1:  # There are checkable tiles vertically upwards and downwards
                        tempUpY = y - 1
                        tempDownY = y + 1
                        upCounter = 1
                        downCounter = 1
                        while checkNeighbors(newBoard, tempUpY, x)[0] == 1:
                            upCounter += 1
                            tempUpY -= 1
                        while checkNeighbors(newBoard, tempDownY, x)[1] == 1:
                            downCounter += 1
                            tempDownY += 1
                        temp = ''
                        for letter in range(tempUpY, tempDownY+1):
                            temp = temp + newBoard[letter][x]
                        print("Vertical Upwards/Downwards Word Check:", end=" ")
                        if temp.upper() in wordDictionary:
                            print("{} is a word!".format(temp))
                        else:
                            print("{} is not a word, BREAK!".format(temp))
                            return False
                    elif neighborTuple[0] == 1:  # There are checkable tiles vertically upwards, not downwards
                        tempUpY = y - 1
                        upCounter = 1
                        while checkNeighbors(newBoard, tempUpY, x)[0] == 1:
                            upCounter += 1
                            tempUpY -= 1
                        temp = ''
                        for letter in range(tempUpY, y+1):
                            temp = temp + newBoard[letter][x]
                        print("Vertical Upwards Word Check:", end=" ")
                        if temp.upper() in wordDictionary:
                            print("{} is a word!".format(temp))
                        else:
                            print("{} is not a word, BREAK!".format(temp))
                            return False
                    elif neighborTuple[1] == 1:  # There are checkable tiles vertically downwards, not upwards
                        tempDownY = y + 1
                        downCounter = 1
                        while checkNeighbors(newBoard, tempDownY, x)[1] == 1:
                            downCounter += 1
                            tempDownY += 1
                        temp = ''
                        for letter in range(y, tempDownY+1):
                            temp = temp + newBoard[letter][x]
                        print("Vertical Downwards Word Check:", end=" ")
                        if temp.upper() in wordDictionary:
                            print("{} is a word!".format(temp))
                        else:
                            print("{} is not a word, BREAK!".format(temp))
                            return False
                    if neighborTuple[2] == 1 and neighborTuple[3] == 1:  # There are checkable tiles horizontally to the left and to the right
                        tempLeftX = x - 1
                        tempRightX = x + 1
                        leftCounter = 1
                        rightCounter = 1
                        while checkNeighbors(newBoard, y, tempLeftX)[2] == 1:
                            leftCounter += 1
                            tempLeftX -= 1
                        while checkNeighbors(newBoard, y, tempRightX)[3] == 1:
                            rightCounter += 1
                            tempRightX += 1
                        temp = ''
                        for letter in range(tempLeftX, tempRightX+1):
                            temp = temp + newBoard[y][letter]
                        print("Horizontal Leftwards/Rightwards Word Check:", end=" ")
                        if temp.upper() in wordDictionary:
                            print("{} is a word!".format(temp))
                        else:
                            print("{} is not a word, BREAK!".format(temp))
                            return False
                    elif neighborTuple[2] == 1:  # There are checkable tiles horizontally to the left, not to the right
                        tempLeftX = x - 1
                        leftCounter = 1
                        while checkNeighbors(newBoard, y, tempLeftX)[2] == 1:
                            leftCounter += 1
                            tempLeftX -= 1
                        temp = ''
                        for letter in range(tempLeftX, x+1):
                            temp = temp + newBoard[y][letter]
                        print("Horizontal Leftwards Word Check:", end=" ")
                        if temp.upper() in wordDictionary:
                            print("{} is a word!".format(temp))
                        else:
                            print("{} is not a word, BREAK!".format(temp))
                            return False
                    elif neighborTuple[3] == 1:  # There are checkable tiles horizontally to the right, not to the left
                        tempRightX = x + 1
                        rightCounter = 1
                        while checkNeighbors(newBoard, y, tempRightX)[3] == 1:
                            rightCounter += 1
                            tempRightX += 1
                        temp = ''
                        for letter in range(x, tempRightX+1):
                            temp = temp + newBoard[y][letter]
                        print("Horizontal Rightwards Word Check:", end=" ")
                        if temp.upper() in wordDictionary:
                            print("{} is a word!".format(temp))
                        else:
                            print("{} is not a word, BREAK!".format(temp))
                            return False
                    print("There were {} checkable tiles up, {} checkable tiles down, {} checkable tiles left, {} checkable tiles right.\n".format(upCounter, downCounter, leftCounter, rightCounter))
            x += 1
        y += 1
    return True

if __name__ == '__main__':
    cont = 0
    boardTimeStart = time.time()
    if checkBoard(emptyBoard, board3) == True:
        print("Board is valid!")
    else:
        print("Board is invalid, try again!")
    print("Board check took {} seconds.".format(time.time() - boardTimeStart))
    while cont == 1:
        temp = str(input('Enter your seven letters as a string (ex: abcdefg): '))
        start = time.time()
        permList = []
        totalPermList = []
        new_temp = ''
        flag = 0
        defFlag = ''
        size_counter = 7
        tempPoints = 0
        bestPoints = 0
        bestWord = ''

        print('\nScanning all permutations of %i letters...' % size_counter)

        for i in permutation(size_counter):
            x = 0
            while x < len(i[0]):
                new_temp = new_temp + temp[i[0][x]]
                x += 1
            permList.append(new_temp)
            new_temp = ''

        '''
        # Beginning of my attempt at understanding board limits and potential placement locations.
        # Ideally, this is an absolutely comprehensive look at the board state to find the
        # highest scoring word that can possibly be played.. but life is never that simple, is it?
        counterX = 0
        counterY = 0
        for row in sampleBoardArray1:
            for element in row:
                if element == ' ':
                    neighborTuple = checkNeighbors(sampleBoardArray1, counterY, counterX)
                    if 1 in neighborTuple: # If this space has a neighbor tile
                        if neighborTuple[0] == 0 and neighborTuple[1] == 0: # Tiles can be placed vertically upwards and downwards
                            tempUpY = counterY - 1
                            tempDownY = counterY + 1
                            upCounter = 1
                            downCounter = 1
                            while checkNeighbors(sampleBoardArray1, tempUpY, counterX)[0] == 0:
                                upCounter += 1
                                tempUpY -= 1
                            while checkNeighbors(sampleBoardArray1, tempDownY, counterX)[1] == 0:
                                downCounter += 1
                                tempDownY += 1
                        elif neighborTuple[0] == 0: # Tiles can be placed vertically upwards, not downwards
                            tempUpY = counterY - 1
                            upCounter = 1
                            while checkNeighbors(sampleBoardArray1, tempUpY, counterX)[0] == 0:
                                upCounter += 1
                                tempUpY -= 1
                        elif neighborTuple[1] == 0: # Tiles can be placed vertically downwards, not upwards
                            tempDownY = counterY + 1
                            downCounter = 1
                            while checkNeighbors(sampleBoardArray1, tempDownY, counterX)[1] == 0:
                                downCounter += 1
                                tempDownY += 1
                        if neighborTuple[2] == 0 and neighborTuple[3] == 0: # Tiles can be placed horizontally to the left and to the right
                            tempLeftX = counterX - 1
                            tempRightX = counterX + 1
                            leftCounter = 1
                            rightCounter = 1
                            while checkNeighbors(sampleBoardArray1, counterY, tempLeftX)[2] == 0:
                                leftCounter += 1
                                tempLeftX -= 1
                            while checkNeighbors(sampleBoardArray1, counterY, tempRightX)[3] == 0:
                                rightCounter += 1
                                tempRightX += 1
                        elif neighborTuple[2] == 0: # Tiles can be placed horizontally to the left, not to the right
                            tempLeftX = counterX - 1
                            leftCounter = 1
                            while checkNeighbors(sampleBoardArray1, counterY, tempLeftX)[2] == 0:
                                leftCounter += 1
                                tempLeftX -= 1
                        elif neighborTuple[3] == 0: # Tiles can be placed horizontally to the right, not to the left
                            tempRightX = counterX + 1
                            rightCounter = 1
                            while checkNeighbors(sampleBoardArray1, counterY, tempRightX)[3] == 0:
                                rightCounter += 1
                                tempRightX += 1
                counterX += 1
            counterY += 1
            counterX = 0
        '''

        for new_temp in permList:
            if '*' in new_temp: # Wildcard Blank. Unsure if that tile will be used in our design though.
                z = 0
                while z < 26:
                    replace_temp = new_temp.replace('*', letterList[z])
                    if replace_temp.upper() in wordDictionary and replace_temp not in totalPermList:
                        totalPermList.append(replace_temp)
                        y = 0
                        tempPoints = 0
                        while y < size_counter:
                            tempPoints = tempPoints + letterPointDict[replace_temp[y]]
                            y += 1
                        if tempPoints > bestPoints:
                            bestPoints = tempPoints + 50
                            bestWord = replace_temp
                            print(bestWord, 'is now the highest scoring word')
                    z += 1
            elif new_temp.upper() in wordDictionary and new_temp not in totalPermList:
                y = 0
                tempPoints = 0
                while y < size_counter:
                    tempPoints = tempPoints + letterPointDict[new_temp[y]]
                    y += 1
                if tempPoints > bestPoints:
                    bestPoints = tempPoints + 50
                    bestWord = new_temp
                    print(bestWord, 'is now the highest scoring word')
        size_counter -= 1
        while size_counter > 1:
            print('\nScanning all permutations of %i letters...' % size_counter)
            for perm in permList:
                new_temp = perm[0:size_counter]
                if '*' in new_temp:  # Wildcard Blank. Unsure if that tile will be used in our design though.
                    z = 0
                    while z < 26:
                        replace_temp = new_temp.replace('*', letterList[z])
                        if replace_temp.upper() in wordDictionary and replace_temp not in totalPermList:
                            totalPermList.append(replace_temp)
                            y = 0
                            tempPoints = 0
                            while y < size_counter:
                                tempPoints = tempPoints + letterPointDict[replace_temp[y]]
                                y += 1
                            if tempPoints > bestPoints:
                                bestPoints = tempPoints
                                bestWord = replace_temp
                                print(bestWord, 'is now the highest scoring word')
                        z += 1
                elif new_temp.upper() in wordDictionary and new_temp not in totalPermList:
                    totalPermList.append(new_temp)
                    y = 0
                    tempPoints = 0
                    while y < size_counter:
                        tempPoints = tempPoints + letterPointDict[new_temp[y]]
                        y += 1
                    if tempPoints > bestPoints:
                        bestPoints = tempPoints
                        bestWord = new_temp
                        print(bestWord, 'is now the highest scoring word')
            size_counter -= 1

        print('\nTime taken:', round(time.time() - start, 6), 'seconds')
        if bestPoints > 0:
            if len(bestWord) >= 7:
                print('Bingo! 50 Bonus Points!')
            if bestPoints > 100:
                print('The best word found was {}, which is worth {} points! What a turn!'.format(bestWord.upper(), bestPoints))
            elif bestPoints > 50:
                print('The best word found was {}, which is worth {} points! Wow!'.format(bestWord.upper(), bestPoints))
            elif bestPoints > 25:
                print('The best word found was {}, which is worth {} points! Good job!'.format(bestWord.upper(), bestPoints))
            else:
                print('The best word found was {}, which is worth {} points!'.format(bestWord.upper(), bestPoints))
            answer = input('Would you like the definition of {}? (y/n): '.format(bestWord))
            while answer != 'y' and answer != 'n':
                answer = input('Please enter y or n. Would you like the definition of {}? (y/n): '.format(bestWord))
            if answer == 'y':
                print(wordDictionary[bestWord.upper()])
        else:
            print('No possible words could be found..')
        temp_cont = input('Next turn? (y/n): ')
        while temp_cont != 'y' and temp_cont != 'n':
            temp_cont = input('Please enter y or n. Next turn? (y/n): ')
        if temp_cont == 'n':
            cont = 0
        '''
        for row in boardArray:
            for element in row:
                if element == '':
                    print('   ', end="")
                else:
                    print(' ', element, ' ', end="")
            print('\n')
        '''