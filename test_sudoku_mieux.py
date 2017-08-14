

import numpy as np
import random
import copy
import time

## REMARQUES
#les indices x et y sont parfois inversés à cause de la convention mathématique (y puis x)
#pour enlever les 0 au debut et fin : np.trim_zeros
# il faudrait changer xIndex et yIndex en hIndex et vIndex...
#Reflechir à si il faut améliorer 2outOf3
#on dirait qu'il est aussi bon que moi...


#pour accelerer :
#modifier la fonction isFinished
#modifier update ?

#pour le rendre plus puissant :
#regarder les techniques qui utilisent les blocs identiques



class Grid (object) :

    def __init__ (self, grid) :
        """ grid corresponds to the "real" grid
            tempGrid corresponds to the grid where the little numbers are written
            Because of python, the third dimension is of length 9 all the time
        """
        self.grid = grid

        tempGrid = np.zeros((9,9,9))
        for k in range (9) :
            for i in range (9) :
                tempGrid[k,i,0] = grid[k,i]
        self.tempGrid = tempGrid

        self.neighborsNbrGrid = np.zeros((9,9))

        self.visitsNbrGrid = np.zeros((9,9))

        self.allTilesHaveBeenVisited = False

    def __str__ (self) :
        string = ""
        string += " -----------------------" + "\n"
        for k in range (9) :
            for i in range (9) :
                if (i==0) or (i == 3) or (i == 6):
                    string += "|" + " "
                if int(self.grid[k,i]) != 0 :
                    string += str(int(self.grid[k,i])) + " "
                else :
                    string += "." + " "
            string += "|"
            string += "\n"
            if (k == 2) or (k==5) :
                string += "|-----------------------|" + "\n"
        string += " -----------------------"
        return string

    def initNeighborsNbrGrid (self) :
        """ A bit costly, but it is meant to be called only once
        """
        for k in range (9) :
            for i in range (9) :
                someTile = self.getTile(k,i)
                if someTile.value != 0 :
                    self.neighborsNbrGrid[k,i] = 0
                else :
                    self.neighborsNbrGrid[k,i] = len(someTile.getNeighbors())

    def updateNeighborsNbrGrid (self, xIndex, yIndex) :
        """ Updates the grid by modifying only one tile
            Meant to be called for all neigbors of a tile that was modified
            Doesn't return anything
        """
        self.neighborsNbrGrid[xIndex, yIndex] = len(self.getTile(xIndex, yIndex).getNeighbors())

    def isFinished(self) :
        """ Verifies that finished grid is correct
            by checking that all sums of blocks, lines and columns equal 45
            Returns : True if grid is correct, False otherwise
        """
        for k in range (9) :
            #currentColumn = myGrid.getColumn(k)
            if (np.sum(myGrid.getColumn(k).column) != 45) :
                return False
            #currentLine = myGrid.getLine(k)
            if (np.sum(myGrid.getLine(k).line) != 45) :
                return False

        for k in range (3) :
            for i in range (3) :
                #currentBlock = myGrid.getBlock(k,i)
                if (np.sum(myGrid.getBlock(k,i).block) != 45) :
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

    def findMostPromising (self) :
        """ Orders the tiles by descending number of neighbors
            Returns an array of size 81x2
        """
        arrayOfNeighbors = self.neighborsNbrGrid.flatten()
        orderedTiles = []
        mostPromising = np.zeros((2,81))
        for k in range (8,-1,-1) :
            orderedTiles += [i for i, j in enumerate(arrayOfNeighbors) if j == k]
        for i, k in enumerate(orderedTiles) :
            mostPromising[0,i] = k//9
            mostPromising[1,i] = k%9
        return(mostPromising)

    def checkIfAllTilesHaveBeenVisited (self) :
        """ Returns True if all tiles have been evaluated at least once, False otherwise
        """
        for k in range (9) :
            for i in range (9) :
                if myGrid.getTile(k,i).value == 0 :
                    if myGrid.visitsNbrGrid[k,i] == 0 :
                        return False
        myGrid.allTilesHaveBeenVisited = True
        return True

    def searchForTwoOutOfThree (self) :
        """
        Searches for lines/columns of blocks in which we know 2 identical numbers
        If found, we put the number in the only case it can fit
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

                    if (np.count_nonzero(tilesStudied) == 2) :
                        #we check if 2 out of 3 tiles are filled
                        #if it is the case we can fill the last one
                        indicesNotZero = np.array(np.nonzero(tilesStudied))
                        if (0 not in indicesNotZero) :
                            tileToModify = myGrid.getTile(3*blockToStudy, columnToStudy)
                        elif (1 not in indicesNotZero) :
                            tileToModify = myGrid.getTile(3*blockToStudy+1, columnToStudy)
                        else :
                            tileToModify = myGrid.getTile(3*blockToStudy+2, columnToStudy)
                        tileToModify.modifyValue(i)

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
                        elif (1 not in indicesNotZero) :
                            tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy+1)
                        else :
                            tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy+2)
                        tileToModify.modifyValue(i)

    def checkAllBlockRowInteraction (self) :
        """ Launches the website method for all the blocks
            Doesn't return anything
            Works but doesn't help on the test difficult grids
            Slows down the easy grids

            A AMELIORER : IL NE FAUT PAS LE FAIRE POUR LES BLOCKS REMPLIS ETC...


        """
        for k in range (3) :
            for i in range (3) :
                currentBlock = self.getBlock(k,i)
                currentBlock.checkOneBlockRowInteraction()



class Block (object) :

    def __init__ (self, block, xIndex, yIndex) :
        self.block = block
        self.xIndex = xIndex
        self.yIndex = yIndex

    def checkIfTrivial (self) :
        """ Returns :
        (True if there is only one number missing, position of number to change, value to put)
        (False, -1, -1 ) otherwise
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

    def checkOneBlockRowInteraction (self) :
        """ Uses the technique seen on the website to narrow possibilities for the lines and columns nearby
            For all unfound numbers, it checks if it is necessarly in the block (respectively to lines and columns)
            Doesn't return anything
        """
        foundNumbers = np.trim_zeros(np.sort((self.block.flatten())))
        unfoundNumbers = []
        for k in range (1, 10):
            if k not in foundNumbers :
                unfoundNumbers.append(k)
        unfoundNumbers = np.array(unfoundNumbers)

        for k in unfoundNumbers :
            #now we have to check if k can only be in a line or a columns
            #ATTENTION : bordel entre la notation XY et la convention mathématique

            possibilitiesInLine = [] #list of the lines numbers in which k is a possibility
            possibilitiesInColumn = [] #list of the columns numbers in which k is a possibility

            for i in range (3) :
                for j in range (3) :
                    currentTileX = 3*self.yIndex+i
                    currentTileY = 3*self.xIndex+j

                    currentPossibilities = myGrid.tempGrid[currentTileX, currentTileY]
                    if k in currentPossibilities :
                        if currentTileX not in possibilitiesInLine :
                            possibilitiesInLine.append(currentTileX)
                        if currentTileY not in possibilitiesInColumn :
                            possibilitiesInColumn.append(currentTileY)

            if len(possibilitiesInLine) == 1 : #it means this number has to be in this block, respectively to the line
                #before modifying anything, we must verify if the number has been found in the neighbor blocks.
                #   In that case, it is useless to proceed (ENCORE A FAIRE)

                lineToStudyIndex = possibilitiesInLine[0]
                for i in range(9) :
                    if i not in [3*self.xIndex, 3*self.xIndex+1, 3*self.xIndex+2] : #in that case we're not in the block, so we must remove k from tempGrid
                        currentTilePossibilities = myGrid.tempGrid[lineToStudyIndex, i]
                        currentTileNewPossibilities = []
                        #the problem is that we must keep the possibilities in order
                        for j in currentTilePossibilities :
                            if j != k :
                                currentTileNewPossibilities.append(j)
                        if len(currentTileNewPossibilities) == 8 :
                            currentTileNewPossibilities.append(0)
                        myGrid.tempGrid[lineToStudyIndex, i] = currentTileNewPossibilities


            if len(possibilitiesInColumn) == 1 : #it means this number has to be in this block, respectively to the column
                #before modifying anything, we must verify if the number has been found in the neighbor blocks.
                #   In that case, it is useless to proceed (ENCORE A FAIRE)

                columnToStudyIndex = possibilitiesInColumn[0]
                for i in range(9) :
                    if i not in [3*self.yIndex, 3*self.yIndex+1, 3*self.yIndex+2] : #in that case we're not in the block, so we must remove k from tempGrid
                        currentTilePossibilities = myGrid.tempGrid[i, columnToStudyIndex]
                        currentTileNewPossibilities = []
                        #the problem is that we must keep the possibilities in order
                        for j in currentTilePossibilities :
                            if j != k :
                                currentTileNewPossibilities.append(j)
                        if len(currentTileNewPossibilities) == 8 :
                            currentTileNewPossibilities.append(0)
                        myGrid.tempGrid[i, columnToStudyIndex] = currentTileNewPossibilities

class Line (object) :

    def __init__ (self, line, index) :
        self.line = line
        self.index = index

    def checkIfTrivial (self) :
        """ Returns :
        (True if there is only one number missing, position of number to change, value to put)
        (False, -1, -1 ) otherwise
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
        """ Returns :
        (True if there is only one number missing, position of number to change, value to put)
        (False, -1, -1 ) otherwise
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
        """ Checks the neighbors of the tile,
            Returns a list of the known neighbors without duplicates
        """
        allNeighbors = []
        allNeighbors.append(myGrid.getBlock(self.yIndex//3, self.xIndex//3).block.flatten())
        allNeighbors.append(myGrid.getLine(self.xIndex).line)
        allNeighbors.append(myGrid.getColumn(self.yIndex).column)
        allNeighbors = np.array(allNeighbors).flatten()
        allNeighborsNoDuplicates = list(set(allNeighbors))
        if 0 in allNeighborsNoDuplicates :
            allNeighborsNoDuplicates.remove(0)
        return(allNeighborsNoDuplicates)

    def evaluate(self) :
        """ Gets the neighbors using getNeighbors
            If there is only one missing, we modify the tile
            If there are multiples choices, we put them in the tempGrid
            Returns : -1 if tile is not 0, True if tile has been modified
        """

        if (self.value != 0) :
            return -1

        myGrid.visitsNbrGrid[self.xIndex, self.yIndex] += 1

        #we first check if there is only one possibility in the tempGrid
        possibilitiesNonZero = np.trim_zeros(myGrid.tempGrid[self.xIndex, self.yIndex])
        if (len(possibilitiesNonZero) == 1) :
            self.modifyValue(myGrid.tempGrid[self.xIndex, self.yIndex, 0])
            return True

        #we now compute the neighbors as usual
        neighbors = np.array(self.getNeighbors())

        if (len(neighbors) == 8) :
            #it means that neighbors only leave one possibility for the tile
            for k in range(1,10) :
                if k not in neighbors :
                    self.modifyValue(k)
                    return True

        elif (len(neighbors) < 8) :
            #if there are multiple possibilities for the tile
            for k in range(1,10) :
                if (k not in neighbors) and (k not in myGrid.tempGrid[self.xIndex, self.yIndex]) :
                    oldPossibilities = np.delete(myGrid.tempGrid[self.xIndex, self.yIndex], 8)
                    myGrid.tempGrid[self.xIndex, self.yIndex] = np.append(k, oldPossibilities)
        else :
            print("ERROR : 9 neighbors")

    def modifyValue (self, value) :
        """ Once we found the value of a tile, we modify it
            We also modify the possible values of all of the neighbors of the tile
            Doesn't return anything
        """

        #we modify the value of the tile
        myGrid.grid[self.xIndex, self.yIndex] = value
        #we remove the possibilities and leave only the real value
        myGrid.tempGrid[self.xIndex, self.yIndex, 0] = value
        myGrid.tempGrid[self.xIndex, self.yIndex, 1:9] = 0

        #we modify the number of neighbors to 0
        myGrid.neighborsNbrGrid[self.xIndex, self.yIndex] = 0

        #we modify the possible values of the neighbors : block
        xIndexBlock = self.yIndex//3
        yIndexBlock = self.xIndex//3

        for k in range (3) :
            for i in range (3) :
                #we go through the block
                possibleTileValues = list(myGrid.tempGrid[3*yIndexBlock+i, 3*xIndexBlock+k])
                currentTile = myGrid.getTile(3*yIndexBlock+i, 3*xIndexBlock+k)
                if (value in possibleTileValues) and (currentTile.value == 0) :
                    #in that case we have to remove "value" from the possibilities
                    possibleTileValues.remove(value)
                    possibleTileValues.append(0)
                    myGrid.tempGrid[3*yIndexBlock+i, 3*xIndexBlock+k] = np.array(possibleTileValues)
                myGrid.updateNeighborsNbrGrid(currentTile.xIndex, currentTile.yIndex)

        #we modify the possible values of the neighbors : line
        for k in range (9) :
            #we go through the line
            possibleTileValues = list(myGrid.tempGrid[self.xIndex, k])
            currentTile = myGrid.getTile(self.xIndex, k)
            if (value in possibleTileValues) and (currentTile.value == 0) :
                #in that case we have to remove "value" from the possibilities
                possibleTileValues.remove(value)
                possibleTileValues.append(0)
                myGrid.tempGrid[self.xIndex, k] = np.array(possibleTileValues)
            myGrid.updateNeighborsNbrGrid(currentTile.xIndex, currentTile.yIndex)

        #we modify the possible values of the neighbors : column
        for k in range (9) :
            #we go through the column
            possibleTileValues = list(myGrid.tempGrid[k, self.yIndex])
            currentTile = myGrid.getTile(k, self.yIndex)
            if (value in possibleTileValues) and (currentTile.value == 0):
                #in that case we have to remove "value" from the possibilities
                possibleTileValues.remove(value)
                possibleTileValues.append(0)
                myGrid.tempGrid[k, self.yIndex] = np.array(possibleTileValues)
            myGrid.updateNeighborsNbrGrid(currentTile.xIndex, currentTile.yIndex)

    def narrowPossibilities(self) :
        """ Once ALL tiles have been evaluated, we can check if the possibilities for one number are only for one tile
            Returns : -1 if the tile is already known, True if the tile is modified
        """

        if (self.value != 0) :
            return -1

        #first we check for the block
        blockPossibilities = np.array(myGrid.tempGrid[(self.xIndex//3)*3 : (self.xIndex//3)*3+3, (self.yIndex//3)*3 : (self.yIndex//3)*3+3])
        blockPossibilities = np.reshape(blockPossibilities, (1,81))
        blockPossibilities = np.sort(blockPossibilities[0])
        blockPossibilities = np.trim_zeros(blockPossibilities)
        #we now have a list of all the possibilities for the tiles from the block
        #if one of the possibilities only appears one, we know where we can put it
        singles = [x for x in list(blockPossibilities) if list(blockPossibilities).count(x) == 1]

        #now we have to check if the singles are part of this tile's possibilities
        for k in singles :
            if k in myGrid.tempGrid[self.xIndex, self.yIndex] :
                self.modifyValue(k)
                return True

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
                self.modifyValue(k)
                return True

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
                self.modifyValue(k)
                return True

    def checkIfTrivial(self) :
        """ We use the three methods checkIfTrivial for the block, line and column the tile belongs to
            Returns :  -1 if tile is already known, True if tile is modified
        """
        if (self.value != 0) :
            return -1

        #for the block
        currentBlock = myGrid.getBlock(self.yIndex//3, self.xIndex//3)
        trivialityArray = currentBlock.checkIfTrivial()
        if trivialityArray[0] == True:
            self.modifyValue(trivialityArray[2])
            return True
        #for the line
        currentLine = myGrid.getLine(self.xIndex)
        trivialityArray = currentLine.checkIfTrivial()
        if trivialityArray[0] == True :
            self.modifyValue(trivialityArray[2])
            return True
        #for the column
        currentColumn = myGrid.getLine(self.yIndex)
        trivialityArray = currentColumn.checkIfTrivial()
        if trivialityArray[0] == True :
            self.modifyValue(trivialityArray[2])
            return True

###############################################################

TEST_GRID_1 = np.array([[  0,  3,  2,  0,  8,  0,  0,  0,  0],
                        [  8,  0,  1,  0,  0,  0,  9,  0,  3],
                        [  0,  0,  0,  6,  0,  3,  0,  0,  0],
                        [  0,  2,  0,  0,  5,  7,  4,  0,  6],
                        [  5,  0,  0,  4,  0,  6,  0,  0,  2],
                        [  7,  0,  4,  8,  3,  0,  0,  9,  0],
                        [  0,  0,  0,  5,  0,  1,  0,  0,  0],
                        [  0,  0,  8,  0,  0,  0,  7,  0,  1],
                        [  4,  0,  0,  0,  7,  0,  6,  3,  0]])

TEST_GRID_2 = np.array([[  0,  0,  2,  0,  0,  0,  0,  0,  0],
                        [  0,  0,  3,  0,  1,  0,  0,  0,  6],
                        [  0,  4,  0,  0,  2,  0,  0,  3,  0],
                        [  1,  0,  0,  0,  0,  3,  0,  0,  9],
                        [  0,  0,  5,  0,  0,  0,  4,  0,  0],
                        [  2,  0,  0,  6,  0,  0,  0,  0,  8],
                        [  0,  9,  0,  0,  7,  0,  0,  4,  0],
                        [  7,  0,  0,  0,  8,  0,  5,  0,  0],
                        [  0,  0,  0,  0,  0,  0,  3,  0,  0]])

TEST_GRID_3 = np.array([[  4,  5,  0,  0,  0,  2,  0,  9,  0],
                        [  3,  0,  7,  4,  0,  0,  1,  0,  0],
                        [  6,  2,  0,  0,  0,  0,  0,  0,  0],
                        [  0,  0,  0,  0,  4,  0,  0,  7,  0],
                        [  0,  6,  0,  9,  7,  0,  0,  8,  0],
                        [  0,  1,  0,  0,  0,  0,  3,  0,  0],
                        [  2,  0,  0,  1,  0,  8,  0,  0,  0],
                        [  1,  0,  5,  0,  0,  0,  0,  0,  3],
                        [  0,  0,  0,  2,  0,  9,  0,  0,  7]])

TEST_GRID_4 = np.array([[  0,  0,  1,  5,  0,  0,  0,  0,  0],
                        [  0,  8,  0,  0,  0,  3,  1,  4,  0],
                        [  0,  4,  0,  0,  8,  0,  0,  0,  3],
                        [  0,  7,  0,  0,  5,  0,  0,  0,  8],
                        [  0,  0,  6,  9,  0,  8,  3,  0,  0],
                        [  3,  0,  0,  0,  2,  0,  0,  5,  0],
                        [  5,  0,  0,  0,  7,  0,  0,  1,  0],
                        [  0,  2,  7,  1,  0,  0,  0,  9,  0],
                        [  0,  0,  0,  0,  0,  4,  5,  0,  0]])

TEST_GRID_5 = np.array([[  8,  0,  0,  0,  0,  0,  0,  0,  0],
                        [  0,  0,  3,  0,  0,  0,  0,  0,  0],
                        [  0,  7,  0,  6,  9,  0,  2,  0,  0],
                        [  0,  5,  0,  0,  0,  7,  0,  0,  0],
                        [  0,  0,  0,  0,  4,  5,  7,  0,  0],
                        [  0,  0,  0,  1,  0,  0,  0,  9,  0],
                        [  0,  0,  1,  0,  0,  0,  0,  0,  8],
                        [  0,  0,  8,  5,  0,  0,  0,  0,  0],
                        [  0,  9,  0,  0,  0,  0,  4,  3,  0]])

TEST_GRID_6 = np.array([[  0,  5,  0,  6,  0,  0,  0,  0,  0],
                        [  0,  0,  0,  9,  0,  0,  0,  0,  2],
                        [  8,  0,  0,  0,  0,  0,  3,  0,  0],
                        [  7,  0,  0,  0,  0,  4,  0,  0,  0],
                        [  0,  9,  0,  0,  0,  0,  0,  6,  0],
                        [  0,  0,  0,  0,  3,  0,  0,  0,  0],
                        [  3,  0,  7,  0,  0,  0,  4,  0,  0],
                        [  0,  0,  0,  2,  0,  0,  0,  9,  0],
                        [  1,  0,  0,  0,  0,  0,  0,  0,  0]])

###############################################################

#Initialisation
TEST_GRID = TEST_GRID_6
METHOD = 1      #1 = smart, 2 = bourrin

###############################################################

myGrid = Grid(copy.deepcopy(TEST_GRID))
print(Grid(TEST_GRID))

startTime = time.time()

if METHOD == 1 :

    # myGrid.initNeighborsNbrGrid()
    # print("Number of neighbors", sum(sum(myGrid.neighborsNbrGrid))) #it can be a good indicator of difficulty

    # a 2-out-3-search doesnt speed up the algorithm :(
    # this first inital "naive" search helps in most cases

    for k in range (9) :
        for i in range (9) :
            myGrid.getTile(k,i).evaluate()

    numberOfPassagesInLoop = 0

    while (myGrid.isFinished() != True and numberOfPassagesInLoop < 500) :
        aTileChanged = False
        mostPromising = myGrid.findMostPromising()
        promisingCounter = 0
        #myGrid.checkAllBlockRowInteraction() #works but slows everything
        while not(aTileChanged) and (myGrid.isFinished() != True) and (promisingCounter < 81) :
            numberOfPassagesInLoop += 1
            xIndex = int(mostPromising[0,promisingCounter])
            yIndex = int(mostPromising[1,promisingCounter])
            averageVisitNumber = np.mean(myGrid.visitsNbrGrid)

            if myGrid.visitsNbrGrid[xIndex, yIndex] > 10 * averageVisitNumber :
                #useful to avoid visiting to often the same tile
                #if the while-loop loops endlessly, rise the coefficient
                promisingCounter += 1

            else :
                someTile = myGrid.getTile(xIndex, yIndex)

                if (someTile.evaluate() == True):
                    aTileChanged = True

                else :
                    if myGrid.allTilesHaveBeenVisited == True :
                        someTile.narrowPossibilities()
                    else :
                        myGrid.checkIfAllTilesHaveBeenVisited()
                    promisingCounter += 1

    print("numberOfPassagesInLoop :", numberOfPassagesInLoop)

if METHOD == 2 :
    compteur = 0
    while (myGrid.isFinished() != True and compteur<5) :
        compteur+=1
        for k in range (9) :
            for i in range (9) :
                someTile = myGrid.getTile(k,i)
                someTile.evaluate()
                if compteur > 1 :
                    someTile.narrowPossibilities()

if METHOD == 3 :

    for k in range (9) :
        for i in range (9) :
            someTile = myGrid.getTile(k,i)
            someTile.evaluate()
    for k in range (9) :
        for i in range (9) :
            someTile = myGrid.getTile(k,i)
            someTile.narrowPossibilities()

    someBlock = myGrid.getBlock(0,1)
    print(someBlock.block)
    someBlock.checkOneBlockRowInteraction()

endTime = time.time()
print(myGrid)
print("Time elapsed :", round(endTime - startTime, 3)*1000, "ms")
