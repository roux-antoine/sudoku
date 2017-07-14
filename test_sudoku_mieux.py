

import numpy as np
import random
import copy

## REMARQUES
#les indices x et y sont parfois inversés à cause de la convention mathématique (y puis x)
#pour enlever les 0 au debut et fin : np.trim_zeros
# il faut changer xIndex et yIndex en hIndex et vIndex...


class Grid (object) :

    def __init__ (self, grid) :
        """ tempGrid corresponds to the grid where the little numbers are written
            Because of python, the third dimension is of length 9 all the time
        """
        self.grid = grid
        someGrid = np.zeros((9,9,9))
        for k in range (9) :
            for i in range (9) :
                someGrid[k,i,0] = grid[k,i]
        self.tempGrid = someGrid
        #self.tempGrid = grid[:,:,np.newaxis] #to make it a 3D array and not 2D

    def __str__ (self) :
        string = ""
        string += " -----------------------" + "\n"
        for k in range (9) :
            for i in range (9) :
                if (i==0) or (i == 3) or (i == 6):
                    string += "|" + " "
                string += str(int(self.grid[k,i])) + " "
            string += "|"
            string += "\n"
            if (k == 2) or (k==5) :
                string += "|-----------------------|" + "\n"
        string += " -----------------------" + "\n"
        return string

    def verify(self) :
        """ verifies that finished grid is correct
            by checking that all sums of blocks, lines and columns equal 45
            returns : True if grid is correct, False otherwise
        """
        for k in range (9) :
            currentColumn = myGrid.getColumn(k)
            if (np.sum(currentColumn.column) != 45) :
                return False
            currentLine = myGrid.getLine(k)
            if (np.sum(currentLine.line) != 45) :
                return False

        for k in range (3) :
            for i in range (3) :
                currentBlock = myGrid.getBlock(k,i)
                if (np.sum(currentBlock.block) != 45) :
                    return False
        return True

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
                            tileToModify = myGrid.getTile(3*blockToStudy,columnToStudy)
                            #myGrid.grid[3*blockToStudy,columnToStudy] = i
                        elif (1 not in indicesNotZero) :
                            tileToModify = myGrid.getTile(3*blockToStudy+1,columnToStudy)
                            #myGrid.grid[3*blockToStudy+1,columnToStudy] = i
                        else :
                            tileToModify = myGrid.getTile(3*blockToStudy+2,columnToStudy)
                            #myGrid.grid[3*blockToStudy+2,columnToStudy] = i
                        tileToModify.modifyValue(tileToModify.xIndex, tileToModify.yIndex, i)
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
                            tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy)
                            #myGrid.grid[lineToStudy, 3*blockToStudy] = i
                        elif (1 not in indicesNotZero) :
                            tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy+1)
                            #myGrid.grid[lineToStudy, 3*blockToStudy+1] = i
                        else :
                            tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy+2)
                            #myGrid.grid[lineToStudy, 3*blockToStudy+2] = i
                        tileToModify.modifyValue(tileToModify.xIndex, tileToModify.yIndex, i)
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
                if (k not in flattenedArray) :
                    valueToPut = k
            return (True, positionOfZero, valueToPut)
        return (False, -1, -1)

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
                if (k not in flattenedArray) :
                    valueToPut = k
            return (True, positionOfZero, valueToPut)
        return (False, -1, -1)

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
                if (k not in flattenedArray) :
                    valueToPut = k
            return (True, positionOfZero, valueToPut)
        return (False, -1, -1)

class Tile (object) :

    def __init__ (self, value, xIndex, yIndex) :
        self.value = value
        self.xIndex = xIndex
        self.yIndex = yIndex

    def getNeighbors(self) :
        """ checks the neighbors of the tile,
            returns a list of the neighbors without duplicates
        """
        allNeighbors = []
        allNeighbors.append(myGrid.getBlock(self.yIndex//3, self.xIndex//3).block.flatten())
        allNeighbors.append(myGrid.getLine(self.xIndex).line)
        allNeighbors.append(myGrid.getColumn(self.yIndex).column)
        allNeighborsFlat = np.array(allNeighbors).flatten()
        allNeighborsNoDuplicates = list(set(allNeighborsFlat))
        allNeighborsNoDuplicates.remove(0)
        return(allNeighborsNoDuplicates)

    def evaluate(self) :
        """ gets the neighbors using getNeighbors
            if there is only one missing, in that case we modify the tiles
            if there are multiples choices, we put them in the tempGrid
            doesn't return anything, except -1 if tile is not 0
        """
        if (self.value != 0) :
            return -1

        #we first check if there is only one possibility in the tempGrid
        possibilitiesNonZero = np.trim_zeros(myGrid.tempGrid[self.xIndex, self.yIndex])
        if (len(possibilitiesNonZero) == 1) :
            self.modifyValue(self.xIndex, self.yIndex, myGrid.tempGrid[self.xIndex, self.yIndex, 0])

        #we now compute the neighbors as usual
        neighbors = np.array(self.getNeighbors())

        if (len(neighbors) == 8) :
            for k in range(1,10) :
                if k not in neighbors :
                    #we modify the value of the tile
                    self.modifyValue(self.xIndex, self.yIndex, k)

        else :
            for k in range(1,10) :
                if (k not in neighbors) and (k not in myGrid.tempGrid[self.xIndex, self.yIndex]) :
                    someArray = np.delete(myGrid.tempGrid[self.xIndex, self.yIndex], 8)
                    myGrid.tempGrid[self.xIndex, self.yIndex] = np.append(k, someArray)

    def modifyValue (self, xIndex, yIndex, value) :
        """ Once we found the value of a tile, we modify it
            We also modify the possible values of all of the neighbors of the tile
        """
        #we modify the value of the tile
        myGrid.grid[self.xIndex, self.yIndex] = value
        myGrid.tempGrid[self.xIndex, self.yIndex, 0] = value
        myGrid.tempGrid[self.xIndex, self.yIndex, 1:9] = 0

        #we modify the possible values of the neighbors : block
        xIndexBlock = self.yIndex//3
        yIndexBlock = self.xIndex//3
        for k in range (3) :
            for i in range (3) :
                possibleTileValuesList = list(myGrid.tempGrid[3*xIndexBlock+k, 3*yIndexBlock+i])
                if (value in possibleTileValuesList) :
                    #in that case we have to remove "value" from the possibilities
                    possibleTileValuesList.remove(value)
                    possibleTileValuesList.append(0)
                    myGrid.tempGrid[3*xIndexBlock+k, 3*yIndexBlock+i] = np.array(possibleTileValuesList)

        #we modify the possible values of the neighbors : line
        for k in range (9) :
            possibleTileValuesList = list(myGrid.tempGrid[xIndex, k])
            if (value in possibleTileValuesList) :
                #in that case we have to remove "value" from the possibilities
                possibleTileValuesList.remove(value)
                possibleTileValuesList.append(0)
                myGrid.tempGrid[xIndex, k] = np.array(possibleTileValuesList)

        #we modify the possible values of the neighbors : column
        # for k in range (9) :
            possibleTileValuesList = list(myGrid.tempGrid[k, yIndex])
            if (value in possibleTileValuesList) :
                #in that case we have to remove "value" from the possibilities
                possibleTileValuesList.remove(value)
                possibleTileValuesList.append(0)
                myGrid.tempGrid[k, yIndex] = np.array(possibleTileValuesList)

    def narrowPossibilities(self) :
        """ Once ALL tiles have been evaluated, we can check if the possibilities for one number are only for one tile
            doesn't return anything, except -1 if the tile is already known
        """

        if (self.value != 0) :
            return -1

        #first we check for the block
        blockPossibilities = np.array(myGrid.tempGrid[(self.xIndex//3)*3 : (self.xIndex//3)*3+3, (self.yIndex//3)*3 : (self.yIndex//3)*3+3])
        # for k in range (9) :
        #     if (len(np.array(np.nonzero(blockPossibilities[k])).flatten()) == 1) :
        #         #meaning if we already know the value of the tile
        #         blockPossibilities[k] = 0
        blockPossibilities = np.reshape(blockPossibilities, (1,81))
        blockPossibilities = np.sort(blockPossibilities[0])
        blockPossibilities = np.trim_zeros(blockPossibilities)
        #we now have a list of all the possibilities for the tiles from the block
        #if one of the possibilities only appears one, we know where we can put it
        singles = [x for x in list(blockPossibilities) if list(blockPossibilities).count(x) == 1]

        #now we have to check if the singles are part of this tile's possibilities
        for k in singles :
            if k in myGrid.tempGrid[self.xIndex, self.yIndex] :
                self.modifyValue(self.xIndex, self.yIndex, k)

        #then we check for the line
        linePossibilities = np.array(myGrid.tempGrid[self.xIndex, :])
        linePossibilities = np.reshape(linePossibilities, (1,81))
        linePossibilities = np.sort(linePossibilities[0])
        linePossibilities = np.trim_zeros(linePossibilities)
        #we now have a list of all the possibilities for the tiles from the line
        #if one of the possibilities only appears one, we know we can put it
        singles = [x for x in list(linePossibilities) if list(linePossibilities).count(x) == 1]

        #now we have to check if the singles are part of this tile's possibilities
        for k in singles :
            if k in myGrid.tempGrid[self.xIndex, self.yIndex] :
                self.modifyValue(self.xIndex, self.yIndex, k)

        #finally we check for the column
        columnPossibilities = np.array(myGrid.tempGrid[:,self.yIndex])
        columnPossibilities = np.reshape(columnPossibilities, (1,81))
        columnPossibilities = np.sort(columnPossibilities[0])
        columnPossibilities = np.trim_zeros(columnPossibilities)
        #we now have a list of all the possibilities for the tiles from the column
        #if one of the possibilities only appears one, we know we can put it
        singles = [x for x in list(columnPossibilities) if list(columnPossibilities).count(x) == 1]

        #now we have to check if the singles are part of this tile's possibilities
        for k in singles :
            if k in myGrid.tempGrid[self.xIndex, self.yIndex] :
                self.modifyValue(self.xIndex, self.yIndex, k)

    def checkIfTrivial(self) :
        """ We use the three methods checkIfTrivial for the block, line and column the tile belongs to
            Doesn't return anything, except -1 if tile is already known
        """
        if (self.value != 0) :
            return -1

        #for the block
        currentBlock = myGrid.getBlock(self.yIndex//3, self.xIndex//3)
        trivialityArray = currentBlock.checkIfTrivial()
        if trivialityArray[0] == True:
            self.modifyValue(self.xIndex, self.yIndex, trivialityArray[2])
        #for the line
        currentLine = myGrid.getLine(self.xIndex)
        trivialityArray = currentLine.checkIfTrivial()
        if trivialityArray[0] == True :
            self.modifyValue(self.xIndex, self.yIndex, trivialityArray[2])
        #for the column
        currentColumn = myGrid.getLine(self.yIndex)
        trivialityArray = currentColumn.checkIfTrivial()
        if trivialityArray[0] == True :
            self.modifyValue(self.xIndex, self.yIndex, trivialityArray[2])

###########################################

# TEST_GRID = np.array([[  0,  4,  7,  27,  36,  45,  54,  63,  72.],
#                       [  1,  5,  8,  28,  37,  46,  55,  64,  73.],
#                       [  2,  6,  3,  29,  38,  47,  56,  65,  74.],
#                       [  3,  9,  1,  30,  39,  48,  57,  66,  75.],
#                       [  4,  8,  1,  31,  40,  49,  58,  67,  76.],
#                       [  5,  7,  2,  32,  41,  50,  59,  68,  77.],
#                       [  6,  1,  4,  33,  42,  51,  60,  69,  78.],
#                       [  7,  2,  5,  34,  43,  52,  61,  70,  79.],
#                       [  8,  3,  9,  35,  44,  53,  62,  71,  80.]])

TEST_GRID_1 = np.array([[  0,  0,  0,  4,  0,  0,  8,  7,  0.],
                        [  0,  4,  7,  0,  9,  2,  0,  5,  0.],
                        [  2,  0,  0,  6,  0,  0,  0,  3,  0.],
                        [  9,  7,  0,  5,  0,  0,  2,  0,  3.],
                        [  5,  0,  8,  0,  2,  4,  7,  0,  6.],
                        [  6,  0,  4,  0,  0,  7,  0,  8,  5.],
                        [  0,  9,  0,  3,  0,  8,  0,  0,  7.],
                        [  0,  0,  3,  2,  4,  0,  1,  6,  0.],
                        [  0,  1,  2,  0,  0,  0,  0,  9,  0.]])

TEST_GRID_2 = np.array([[  0,  3,  2,  0,  8,  0,  0,  0,  0.],
                        [  8,  0,  1,  0,  0,  0,  9,  0,  3.],
                        [  0,  0,  0,  6,  0,  3,  0,  0,  0.],
                        [  0,  2,  0,  0,  5,  7,  4,  0,  6.],
                        [  5,  0,  0,  4,  0,  6,  0,  0,  2.],
                        [  7,  0,  4,  8,  3,  0,  0,  9,  0.],
                        [  0,  0,  0,  5,  0,  1,  0,  0,  0.],
                        [  0,  0,  8,  0,  0,  0,  7,  0,  1.],
                        [  4,  0,  0,  0,  7,  0,  6,  3,  0.]])

TEST_GRID_3 = np.array([[  8,  0,  0,  0,  0,  0,  0,  0,  0.],
                        [  0,  0,  3,  0,  0,  0,  0,  0,  0.],
                        [  0,  7,  0,  6,  9,  0,  2,  0,  0.],
                        [  0,  5,  0,  0,  0,  7,  0,  0,  0.],
                        [  0,  0,  0,  0,  4,  5,  7,  0,  0.],
                        [  0,  0,  0,  1,  0,  0,  0,  9,  0.],
                        [  0,  0,  1,  0,  0,  0,  0,  0,  8.],
                        [  0,  0,  8,  5,  0,  0,  0,  0,  0.],
                        [  0,  9,  0,  0,  0,  0,  4,  3,  0.]])

TEST_GRID = TEST_GRID_2

myGrid = Grid(copy.deepcopy(TEST_GRID))

compteur = 0
while (myGrid.verify() != True and compteur<3) :
    compteur+=1
    for k in range (9) :
        for i in range (9) :
            myGrid.searchForTwoOutOfThree()
            someTile = myGrid.getTile(i,k)
            someTile.evaluate()

print(Grid(myGrid.grid - TEST_GRID))
print(myGrid)

for k in range (9) :
    for i in range (9) :
        someTile = myGrid.getTile(i,k)
        someTile.checkIfTrivial()
print(myGrid)
