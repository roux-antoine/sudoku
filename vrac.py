


                    # else :
                    #     #we have to check if there is only one possibility for the number, considering the tempGrid
                    #     threeTilesPossibilities = np.array(myGrid.tempGrid[3*blockToStudy:3*blockToStudy+3, columnToStudy])
                    #     threeTilesPossibilities = np.reshape(threeTilesPossibilities, (1,27))
                    #     threeTilesPossibilities = np.sort(threeTilesPossibilities[0])
                    #     threeTilesPossibilities = np.trim_zeros(threeTilesPossibilities)
                    #     #if one of the possibilities only appears one, we know we can put it
                    #     singles = [x for x in list(threeTilesPossibilities) if list(threeTilesPossibilities).count(x) == 1]
                    #
                    #     #now we have to check if the singles are part of this tile's possibilities
                    #     if i in singles :
                    #         #if there is only one possibility for the number
                    #         #we have to find its position and modify the tile's value
                    #         if i in myGrid.tempGrid[3*blockToStudy, columnToStudy] :
                    #             tileToModify = myGrid.getTile(3*blockToStudy, columnToStudy)
                    #         elif i in myGrid.tempGrid[3*blockToStudy+1, columnToStudy] :
                    #             tileToModify = myGrid.getTile(3*blockToStudy+1, columnToStudy)
                    #         else :
                    #             tileToModify = myGrid.getTile(3*blockToStudy+2, columnToStudy)
                    #         tileToModify.modifyValue(i)


                    # else :
                    #     #we have to check if there is only one possibility for the number, considering the tempGrid
                    #     threeTilesPossibilities = np.array(myGrid.tempGrid[lineToStudy, 3*blockToStudy:3*blockToStudy+3])
                    #     threeTilesPossibilities = np.reshape(threeTilesPossibilities, (1,27))
                    #     threeTilesPossibilities = np.sort(threeTilesPossibilities[0])
                    #     threeTilesPossibilities = np.trim_zeros(threeTilesPossibilities)
                    #     #if one of the possibilities only appears one, we know we can put it
                    #     singles = [x for x in list(threeTilesPossibilities) if list(threeTilesPossibilities).count(x) == 1]
                    #     #now we have to check if the singles are part of this tile's possibilities
                    #     if i in singles :
                    #         #if there is only one possibility for the number
                    #         #we have to find its position and modify the tile's value
                    #         if i in myGrid.tempGrid[lineToStudy, 3*blockToStudy] :
                    #             tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy)
                    #         elif i in myGrid.tempGrid[lineToStudy, 3*blockToStudy+1] :
                    #             tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy+1)
                    #         else :
                    #             tileToModify = myGrid.getTile(lineToStudy, 3*blockToStudy+2)
                    #         tileToModify.modifyValue(i)
