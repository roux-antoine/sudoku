

import numpy as np

class Grid (object) :

    def __init__(self, grid) :
        self.grid = grid

        self.bloc0 = grid[0:3][0:3]
        self.bloc1 = grid[0:3][4:6]
        self.bloc2 = grid[0:3][6:9]
        self.bloc3 = grid[3:6][0:3]
        self.bloc4 = grid[3:6][3:6]
        self.bloc5 = grid[3:6][6:9]
        self.bloc6 = grid[6:9][0:3]
        self.bloc7 = grid[6:9][3:6]
        self.bloc7 = grid[6:9][6:9]


        self.line0 = grid[0][:]
        self.line1 = grid[1][:]
        self.line2 = grid[2][:]
        self.line3 = grid[3][:]
        self.line4 = grid[4][:]
        self.line5 = grid[5][:]
        self.line6 = grid[6][:]
        self.line7 = grid[7][:]
        self.line8 = grid[8][:]

        self.column0  = grid[:][0]
        self.column1  = grid[:][1]
        self.column2  = grid[:][2]
        self.column3  = grid[:][3]
        self.column4  = grid[:][4]
        self.column5  = grid[:][5]
        self.column6  = grid[:][6]
        self.column7  = grid[:][7]
        self.column8  = grid[:][8]

        self.tile0 = grid[0][0]
        self.tile1 = grid[0][1]
        self.tile2 = grid[0][2]
        self.tile3 = grid[0][3]
        self.tile4 = grid[0][4]
        self.tile5 = grid[0][5]
        self.tile6 = grid[0][6]
        self.tile7 = grid[0][7]
        self.tile8 = grid[0][8]
        self.tile9 = grid[1][0]#
        self.tile10 = grid[1][1]
        self.tile11 = grid[1][2]
        self.tile12 = grid[1][3]
        self.tile13 = grid[1][4]
        self.tile14 = grid[1][6]
        self.tile15 = grid[1][7]
        self.tile16 = grid[1][8]
        self.tile17 = grid[2][0] #
        self.tile18 = grid[2][1]
        self.tile19 = grid[2][2]
        self.tile20 = grid[2][3]
        self.tile21 = grid[2][4]
        self.tile22 = grid[2][5]
        self.tile23 = grid[2][6]
        self.tile24 = grid[2][7]
        self.tile25 = grid[2][8]
        self.tile26 = grid[3][0] #
        self.tile27 = grid[3][1]
        self.tile28 = grid[3][2]
        self.tile29 = grid[3][3]
        self.tile30 = grid[3][4]
        self.tile31 = grid[3][5]
        self.tile32 = grid[3][6]
        self.tile33 = grid[3][7]
        self.tile34 = grid[3][8]
        self.tile35 = grid[4][0] #
        self.tile36 = grid[4][1]
        self.tile37 = grid[4][2]
        self.tile38 = grid[4][3]
        self.tile39 = grid[4][4]
        self.tile40 = grid[4][5]
        self.tile41 = grid[4][6]
        self.tile42 = grid[4][7]
        self.tile43 = grid[4][8]





TEST_GRID = np.zeros((9,9))
compteur = 0
for k in range (9) :
    for i in range(9) :
        compteur += 1
        TEST_GRID[k][i] = compteur

print(TEST_GRID)

myGrid = Grid(TEST_GRID)

print(myGrid.line8)
