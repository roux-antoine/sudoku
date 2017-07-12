

import numpy as np
import random
import copy

class Grid (object) :

    def __init__ (self, grid) :
        self.grid = grid

    #def getBlock (self, myIndex) :
        #index1 = 0 + 3 * (myIndex // 3)
        #index2 = 3 + 3 * (myIndex // 3)
        #index3 = 0 + 3 * (myIndex % 3)
        #index4 = 3 + 3 * (myIndex % 3)
        #return Block(self.grid[index1:index2, index3:index4], myIndex)

    def getBlock (self, xIndex, yIndex) :
        index1 = 3 * yIndex
        index2 = 3 + 3 * yIndex
        index3 = 3 * xIndex
        index4 = 3 + 3 * xIndex
        return Block(self.grid[index1:index2, index3:index4], xIndex, yIndex)

    def getLine (self, myIndex) :
        return Line(self.grid[myIndex, :], myIndex)

    def getColumn (self, myIndex) :
        return Column(self.grid[:, myIndex], myIndex)

    def getTile (self, xIndex, yIndex) :
        return Tile(self.grid[xIndex, yIndex], xIndex, yIndex)

    def searchForTwoOutOfThree (self) :
        """
        searches for lines/columns of blocks in which we know 2 identical numbers
        if found, we put them where they belong
        """
        #vertically
        for k in range (3) :
            #one for each group of 3 columns
            for i in range (1, 10) :
                numberOfOccurences = 0
                columnsWhereFound = []
                blocksWhereFound = []
                for j in range (3) :
                    #one for each of column of the groups
                    currentColumn = self.getColumn(3*k+j)

                    if (i in currentColumn.column) :
                        numberOfOccurences += 1
                        columnsWhereFound.append(3*k+j)
                        columnInList = currentColumn.column.tolist() #we use "tolist" because index doesnt work on ndarrays
                        blocksWhereFound.append(columnInList.index(i)//3)

                if (numberOfOccurences == 2) :
                    #In that case we have to find if the number of possibilities for the third number in
                    #the group of 3 columns is equal to 1

                    #We find the column and block to study
                    if (3*k not in columnsWhereFound) :
                        columnToStudy = 3*k
                    elif (3*k+1 not in columnsWhereFound) :
                        columnToStudy = 3*k+1
                    else :
                        columnToStudy = 3*k+2

                    if (0 not in blocksWhereFound) :
                        blockToStudy = 0
                    elif (1 not in blocksWhereFound) :
                        blockToStudy = 1
                    else :
                        blockToStudy = 2

                    #We find the 3 vertically aligned tiles to study
                    blockStudied = myGrid.getBlock(k, blockToStudy)
                    tilesStudied = blockStudied.block[:, columnToStudy%3]

                    #Now we check if 2 out of 3 tiles are filled
                    #if it is the case we can fill the last one
                    if (np.count_nonzero(tilesStudied) == 2) :
                        indicesNotZero = np.array(np.nonzero(tilesStudied))
                        if (0 not in indicesNotZero) :
                            myGrid.grid[3*blockToStudy,columnToStudy] = i
                        elif (1 not in indicesNotZero) :
                            myGrid.grid[3*blockToStudy+1,columnToStudy] = i
                        else :
                            myGrid.grid[3*blockToStudy+2,columnToStudy] = i
                        #print("modified : ", i)
                #il reste encore à gérer le cas où les deux autres tuiles ont encore plusieurs possibilités mais qu'on peut quand même conclure

        #horizontally
        for k in range (3) :
            #one for each group of 3 lines
            for i in range (1, 10) :
                numberOfOccurences = 0
                linesWhereFound = []
                blocksWhereFound = []
                for j in range (3) :
                    #one for each of column of the groups
                    currentLine = self.getLine(3*k+j)

                    if (i in currentLine.line) :
                        numberOfOccurences += 1
                        linesWhereFound.append(3*k+j)
                        lineInList = currentLine.line.tolist() #we use "tolist" because index doesnt work on ndarrays
                        blocksWhereFound.append(lineInList.index(i)//3)

                if (numberOfOccurences == 2) :
                    #In that case we have to find if the number of possibilities for the third number in
                    #the group of 3 columns is equal to 1
                    #We find the column and block to study
                    if (3*k not in linesWhereFound) :
                        lineToStudy = 3*k
                    elif (3*k+1 not in linesWhereFound) :
                        lineToStudy = 3*k+1
                    else :
                        lineToStudy = 3*k+2
                    if (0 not in blocksWhereFound) :
                        blockToStudy = 0
                    elif (1 not in blocksWhereFound) :
                        blockToStudy = 1
                    else :
                        blockToStudy = 2

                    #We find the 3 vertically aligned tiles to study
                    blockStudied = myGrid.getBlock(blockToStudy, k)
                    tilesStudied = blockStudied.block[lineToStudy%3]

                    #Now we check if 2 out of 3 tiles are filled
                    #if it is the case we can fill the last one
                    if (np.count_nonzero(tilesStudied) == 2) :
                        indicesNotZero = np.array(np.nonzero(tilesStudied))
                        if (0 not in indicesNotZero) :
                            myGrid.grid[lineToStudy, 3*blockToStudy] = i
                        elif (1 not in indicesNotZero) :
                            myGrid.grid[lineToStudy, 3*blockToStudy+1] = i
                        else :
                            myGrid.grid[lineToStudy, 3*blockToStudy+2] = i
                        print("modified : ", i)
                #il reste encore à gérer le cas où les deux autres tuiles ont encore plusieurs possibilités mais qu'on peut quand même conclure

class Block (object) :

    def __init__ (self, block, xIndex, yIndex) :
        self.block = block
        self.xIndex = xIndex
        self.yIndex = yIndex

    def checkIfTrivial (self) :
        """ returns :
           true if there is only one number missing, false otherwise
           position of number to change
           value to put
        """
        flattenedArray = self.block
        numberOfZeros = np.count_nonzero(flattenedArray)
        if numberOfZeros == 8 :
            positionOfZero = np.argmin(flattenedArray)
            for k in range (1,10) :
                #print(k in flattenedArray)
                if (k not in flattenedArray) :
                    valueToPut = k
            return (True, positionOfZero, valueToPut)
        return False

class Line (object) :

    def __init__ (self, line, index) :
        self.line = line
        self.index = index

    def checkIfTrivial (self) :
        """ returns :
           true if there is only one number missing, false otherwise
           position of number to change
           value to put
        """
        flattenedArray = self.line
        numberOfZeros = np.count_nonzero(flattenedArray)
        if numberOfZeros == 8 :
            positionOfZero = np.argmin(flattenedArray)
            for k in range (1,10) :
                #print(k in flattenedArray)
                if (k not in flattenedArray) :
                    valueToPut = k
            return (True, positionOfZero, valueToPut)
        return False

class Column (object) :

    def __init__ (self, column, index) :
        self.column = column
        self.index = index

    def checkIfTrivial (self) :
        """ returns :
           true if there is only one number missing, false otherwise
           position of number to change
           value to put
        """
        flattenedArray = self.column
        numberOfZeros = np.count_nonzero(flattenedArray)
        if numberOfZeros == 8 :
            positionOfZero = np.argmin(flattenedArray)
            for k in range (1,10) :
                #print(k in flattenedArray)
                if (k not in flattenedArray) :
                    valueToPut = k
            return (True, positionOfZero, valueToPut)
        return False

class Tile (object) :

    def __init__ (self, value, xIndex, yIndex) :
        self.value = value
        self.xIndex = xIndex
        self.yIndex = yIndex

    def checkSurroundings(self) :
        pass


###########################################

TEST_GRID = np.zeros((9,9))
compteur = 0
for k in range (9) :
    for i in range(9) :
        TEST_GRID[i, k] = compteur
        compteur += 1
        #TEST_GRID[k, i] = random.randint(0,9)

# TEST_GRID = np.array([[  0,  4,  7,  27,  36,  45,  54,  63,  72.],
#                       [  1,  5,  8,  28,  37,  46,  55,  64,  73.],
#                       [  2,  6,  3,  29,  38,  47,  56,  65,  74.],
#                       [  3,  9,  1,  30,  39,  48,  57,  66,  75.],
#                       [  4,  8,  1,  31,  40,  49,  58,  67,  76.],
#                       [  5,  7,  2,  32,  41,  50,  59,  68,  77.],
#                       [  6,  1,  4,  33,  42,  51,  60,  69,  78.],
#                       [  7,  2,  5,  34,  43,  52,  61,  70,  79.],
#                       [  8,  3,  9,  35,  44,  53,  62,  71,  80.]])


TEST_GRID = np.array([[  0,  0,  0,  4,  0,  0,  8,  7,  0.],
                      [  0,  4,  7,  0,  9,  2,  0,  5,  0.],
                      [  2,  0,  0,  6,  0,  0,  0,  3,  0.],
                      [  9,  7,  0,  5,  0,  0,  2,  0,  3.],
                      [  5,  0,  8,  0,  2,  4,  7,  0,  6.],
                      [  6,  0,  4,  0,  0,  7,  0,  8,  5.],
                      [  0,  9,  0,  3,  0,  8,  0,  0,  7.],
                      [  0,  0,  3,  2,  4,  0,  1,  6,  0.],
                      [  0,  1,  2,  0,  0,  0,  0,  9,  0.]])

print(TEST_GRID)

myGrid = Grid(copy.deepcopy(TEST_GRID))

#print(myGrid.getBlock(3))
#print(myGrid.getTile(0,7))
#print(myGrid.getBlock(1,0).block)
myGrid.searchForTwoOutOfThree()
print(myGrid.grid - TEST_GRID)
