"""
15-110 Hw6 - Battleship Project
Name: Abhi Yadagiri
AndrewID: ayadagir
"""

import hw6_battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
#5 [Check6-1] & #3 [Check6-2] & #3 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["rows"] = 10
    data["cols"] = 10
    data["boardSize"] = 500
    data["cellSize"] = 50
    data["numShips"] = 5
    data["userBoard"] = emptyGrid(data["rows"], data["cols"])
    data["compBoard"] = emptyGrid(data["rows"], data["cols"])
    data["compBoard"] = addShips(data["compBoard"], data["numShips"])
    data["tempShip"] = []
    data["numAddedShips"] = 0
    data["winner"] = None
    data["maxTurns"] = 50
    data["currTurns"] = 0
    return None


'''
makeView(data, userCanvas, compCanvas)
#6 [Check6-1] & #2 [Check6-2] & #3 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data["cellSize"], userCanvas, data["userBoard"], True)
    drawGrid(data["cellSize"], compCanvas, data["compBoard"], False)
    drawShip(data["cellSize"], userCanvas, data["tempShip"])
    if data["winner"] == "user":
        drawGameOver(data["winner"], userCanvas)
    if data["winner"] == "comp":
        drawGameOver(data["winner"], compCanvas)
    if data["winner"] == "draw":
        drawGameOver(data["winner"], userCanvas)
    return None


'''
keyPressed(data, events)
#5 [Hw6]
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym == "Return":
        makeModel(data)
    pass


'''
mousePressed(data, event, board)
#5 [Check6-2] & #1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"] == None:
        lst = getClickedCell(data, event)
        if board == "user":
            clickUserBoard(data, lst[0], lst[1])
        else:
            if data["numAddedShips"] == 5:
                runGameTurn(data, lst[0], lst[1])
    pass

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
#1 [Check6-1]
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    grid = []
    for row in range(rows):
        x = []
        for col in range(cols):
            x.append(1)
        grid.append(x)
    return grid


'''
createShip()
#2 [Check6-1]
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    row = random.randint(1, 8)
    col = random.randint(1, 8)
    x = random.randint(0, 1)
    ship = []
    if x == 0:
        ship.append([row - 1, col])
        ship.append([row, col])
        ship.append([row + 1, col])
    else:
        ship.append([row, col - 1])
        ship.append([row, col])
        ship.append([row, col + 1])
    return ship


'''
checkShip(grid, ship)
#3 [Check6-1]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    count = 0
    for row in range(len(ship)):
        if grid[ship[row][0]][ship[row][1]] == EMPTY_UNCLICKED:
            count += 1
    if count == 3:
        return True
    else:
        return False


'''
addShips(grid, numShips)
#4 [Check6-1]
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count = 0
    while count < numShips:
        ship = createShip()
        if checkShip(grid, ship) == True:
            for row in range(len(ship)):
                grid[ship[row][0]][ship[row][1]] = SHIP_UNCLICKED
            count += 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
#6 [Check6-1] & #1 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''

def drawGrid(data, canvas, grid, showShips):
    for row in range(len(grid)):
        top = row * data
        bottom = top + data
        for col in range(len(grid[row])):
            left = col * data
            right = left + data
            canvas.create_rectangle(left, top, right, bottom, fill = "blue")
            if grid[row][col] == SHIP_UNCLICKED:
                canvas.create_rectangle(left, top, right, bottom, fill = "yellow")
                if showShips == False:
                    canvas.create_rectangle(left, top, right, bottom, fill = "blue")
            if grid[row][col] == SHIP_CLICKED:
                canvas.create_rectangle(left, top, right, bottom, fill = "red")
            if grid[row][col] == EMPTY_CLICKED:
                canvas.create_rectangle(left, top, right, bottom, fill = "white")
    return None


### WEEK 2 ###

'''
isVertical(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    lst = []
    for row in range(len(ship)):
        lst.append(ship[row][0])
        lst.sort()
    if lst[1] - lst[0] == 1 and lst[2] - lst[1] == 1 and lst[2] - lst[0] == 2 and ship[0][1] == ship[1][1] == ship[2][1] and len(ship) == 3:
        return True
    else:
        return False


'''
isHorizontal(ship)
#1 [Check6-2]
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    lst = []
    for row in range(len(ship)):
        lst.append(ship[row][1])
        lst.sort()
    if lst[1] - lst[0] == 1 and lst[2] - lst[1] == 1 and lst[2] - lst[0] == 2  and ship[0][0] == ship[1][0] == ship[2][0] and len(ship) == 3:
        return True
    else:
        return False


'''
getClickedCell(data, event)
#2 [Check6-2]
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    lst = []
    for row in range(data["rows"]):
        top = row * data["cellSize"]
        bottom = top + data["cellSize"]
        for col in range(data["cols"]):
            left = col * data["cellSize"]
            right = left + data["cellSize"]
            if event.x >= left and event.y >= top and event.x <= right and event.y <= bottom:
                lst.append(row)
                lst.append(col)
    return lst


'''
drawShip(data, canvas, ship)
#3 [Check6-2]
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for row in range(len(ship)):
        top = ship[row][0] * data
        bottom = top + data
        left = ship[row][1] * data
        right = left + data
        canvas.create_rectangle(left, top, right, bottom, fill = "white")
    return None


'''
shipIsValid(grid, ship)
#4 [Check6-2]
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if checkShip(grid, ship) == True and (isVertical(ship) == True or isHorizontal(ship) == True):
        return True
    else:
        return False


'''
placeShip(data)
#4 [Check6-2]
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["userBoard"], data["tempShip"]) == True:
        for coords in data["tempShip"]:
            row = coords[0]
            col = coords[1]
            data["userBoard"][row][col] = SHIP_UNCLICKED
        data["numAddedShips"] += 1
        data["tempShip"] = []
    else:
        print("That ship cannot be placed! Try again.")
        data["tempShip"] = []
    return None


'''
clickUserBoard(data, row, col)
#4 [Check6-2]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["numAddedShips"] == 5:
        return None
    data["tempShip"].append([row, col])
    if len(data["tempShip"]) == 3:
        placeShip(data)
        if data["numAddedShips"] == 5:
            print("Now you can start playing!")
    return None


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
#1 [Hw6] & #3 [Hw6]
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    if board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
    if isGameOver(board) == True:
        data["winner"] = player
    return None


'''
runGameTurn(data, row, col)
#1 [Hw6] & #2 [Hw6] & #4 [Hw6]
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if data["compBoard"][row][col] == SHIP_CLICKED or data["compBoard"][row][col] == EMPTY_CLICKED:
        return None
    else:
        updateBoard(data, data["compBoard"], row, col, "user")
        guess = getComputerGuess(data["userBoard"])
        updateBoard(data, data["userBoard"], guess[0], guess[1], "comp")
        data["currTurns"] += 1
    if data["currTurns"] >= data["maxTurns"]:
        data["winner"] = "draw"
    return None


'''
getComputerGuess(board)
#2 [Hw6]
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    lst = []
    currBool = False
    while currBool == False:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        if board[row][col] == EMPTY_UNCLICKED or board[row][col] == SHIP_UNCLICKED:
            currBool = True
            lst.append(row)
            lst.append(col)
    return lst


'''
isGameOver(board)
#3 [Hw6]
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == SHIP_UNCLICKED:
                return False
    return True


'''
drawGameOver(data, canvas)
#3 [Hw6] & #4 [Hw6] & #5 [Hw6]
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data == "user":
        canvas.create_rectangle(0, 0, 500, 500, fill = "green")
        canvas.create_text(250, 250, text = "YOU WIN!!!", font = "Arial 60")
        canvas.create_text(250, 350, text = "Press ENTER to play again!", font = "Arial 20")
    if data == "comp":
        canvas.create_rectangle(0, 0, 500, 500, fill = "red")
        canvas.create_text(250, 225, text = "HAHAHA TAKE THE L", font = "Arial 35")
        canvas.create_text(250, 275, text = "LOSER!!!", font = "Arial 35")
        canvas.create_text(250, 375, text = "Press ENTER to play again!", font = "Arial 20")
    if data == "draw":
        canvas.create_rectangle(0, 0, 500, 500, fill = "yellow")
        canvas.create_text(250, 225, text = "OUT OF MOVES!", font = "Arial 45")
        canvas.create_text(250, 275, text = "IT'S A DRAW!!!", font = "Arial 45")
        canvas.create_text(250, 375, text = "Press ENTER to play again!", font = "Arial 20")
    return None


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()


    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()


    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
