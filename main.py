import numpy as np
### This is a rudimentary Minesweeper program that I made to test out a theoretical AI on solving the Minesweeper game.
### The interface is text based, and when ran, the user must input the coordinates 0-8,0-8,f in the order of row colonm, and whether to flag the the square if a mineMines is predicted
### Currently cannot implement the AI in terms of using constraints, a safe list, a mines list due to incorrect implementation
###
### Author: Anirban Chakraborty

class Square(object): #a unit of the board, contains the information to whether the user selected it, whether its has a mines, or flagged
    def __init__(self, empty = False, mine = False , flag = False):
        self.empty = empty
        self.mine = mine
        self.flag = flag

    def revealIt(self): #if the user clicked it or not
        self.empty = True
        
    def mineIt(self): #if it has a mine , need to have a different name than the variable
        self.mine = True

    def flagIt(self): #if the user flagged it
        self.flag = True


class Minesweeper(tuple):
    global coordinates
    coordinates = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)) #does not contain 0,0 because that is picked sqaure
    
    def __init__(self, tuple): #making the board out of tuples. easy data structure of of a double array made of tuples
        tuple.__init__(self) #inherting the class of tuples
        self.active = True #when the minesweeper is created, it starts automatically
    
    def minesReveal(self, row, col):
        square = self[row][col]
        adjacentSqs = ((row + adjRow, col + adjCol) for (adjRow, adjCol) in coordinates) #locations of tuples that surround the picked square
        clues = sum(1 for (adjRow, adjCol) in adjacentSqs if (self.check(adjRow, adjCol) and (self[adjRow][adjCol].mine == True))) # sum of all the mines around the picked square
        if (square.empty == False):
            square.revealIt()  #confirms that the square is a mine, not empty
            if(square.mine == True):
                self.active = False #ends the game
            elif (clues == 0): #reveals the clue around the board
                for (adjRow, adjCol) in adjacentSqs:
                    if (self.check(adjRow, adjCol) == True):
                        self.revealIt(adjRow, adjCol) 
    
    def minesFlag(self, row, col): #the tuple's flag becomes active, user can still pick the square.
        if(self[row][col].empty == False): #prevents flag being placed if its already picked
            self[row][col].flagIt()
            
    def mineMines(self, row, col):#enable a square to have a mine, CAN still be empty, since empty only checks if user clicked on square
        self[row][col].mineIt()
        
    def check(self, row, col): #preventing out of bounds exceptions
        if(row >= 0 and row < len(self)):
            if(col >=0 and col < len(self)):
                return True
        return False
    
    def gui(self,row, col): #fills the board with the respective info when displayed. 
        adjacentSqs = ((row + adjRow, col + adjCol) for (adjRow, adjCol) in coordinates) #locations of tuples that surround the picked square
        clues = sum(1 for (adjRow, adjCol) in adjacentSqs if (self.check(adjRow, adjCol) and (self[adjRow][adjCol].mine == True))) # sum of all the mines around the picked square
        if(self[row][col].empty == True): #must be revealed
            if(self[row][col].mine == True):#if mine
                return "M"
            else:
                return str(clues) if(clues == True) else " " #if empty, no hints
        elif(self[row][col].flag == True): #if flagged
            return "F"
        else:
            return "?"
    
    def __str__(self): #overrides print with custom text-based output
        ms = ""
        for (square, row) in enumerate(self):
            ms += ("\n" + str(square) + " " +  "".join(self.gui(square, col) for (col, _) in enumerate(row)) +" " + str(square))
        ms += "\n  " + "".join([str(i) for i in range(len(self))])
        return ms


mines = 3 #mondify num of mines. board is always 10x10 in size
ms = Minesweeper(tuple([tuple([Square() for i in range(9)]) for j in range(9)])) #creates the game board
squares = list(range(64))
for i in range(mines): #inserting mines. random positions
    square = np.random.choice(squares)
    squares.remove(square)
    (row, col) = (square % 9, square // 9)
    ms.mineMines(row, col)
print(ms)
while(ms.active == True): #starts the game
    (row, col, flag) = input("col/row/f(if no flag, enter n | e.g 01f or 44n")
    row = int(row)
    col = int(col)
    if(flag == "n"):
        ms.minesReveal(row, col) #reveals the square. game ends if the square is a M.
    else:
        ms.minesFlag(row, col) #flags the square. Keep track of how many mines, need some sort of mine tracker.
    print(ms)
