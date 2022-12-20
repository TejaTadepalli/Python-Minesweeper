from tkinter import Button,Label
import variables as var
import random                                   # we will use this to select the mines randomly
import ctypes                                   # we will use this to show the message box of GAME OVER
import sys                                      # we will use this to exit the game

class Cell:
    all=[]                                      # this will be a list of all the cells
    cellCountLabelObject = None                 # we will make it global so that we can use it in the main.py file
    cellCount = var.gridSize**2                 # this will be the total number of cells
    
    def __init__(self,x,y,isMine=False):
        self.isMine = isMine
        self.cell_button = None
        self.isOpened = False
        self.isMineCandidate = False                  # this will be used to mark the cell as a mine candidate
        self.x = x                              # x & y are the coordinates of the button
        self.y = y
        Cell.all.append(self)                   # this will append the cell to the list of all the cells
    
    def createButton(self,location):            # this will be creating an instance of the button
        btn = Button(
            location,                           # we will give the location of the button
            width=12,
            height=4,
            # text=f'{self.x},{self.y}',        # this will print the coordinates of the button
        )
        btn.bind("<Button-1>", self.leftClick)  # left click & Button-1 is as per convention 
                                                # we are not calling the function, we are just passing the function as reference
        btn.bind("<Button-3>", self.rightClick) # right click & Button-3 is as per convention
        
        self.cell_button = btn
    
    # this method will be creating the label for the number of cells left
    # and hence will be a ONE-TIME (STATIC) method
    @staticmethod
    def cellCountLabel(location):                   # this will be creating the label for the number of left
        lbl = Label(
            location,
            text=f'Cells Left: {Cell.cellCount}',
            width=12,
            height=4,
            bg="black",
            fg="white",
            font=("Arial", 30, "bold")
        )
        #return lbl
        Cell.cellCountLabelObject = lbl
    
    def leftClick(self,event):
        #print(event)                           
        # # this will print the event, which is basically the button click
        # <ButtonPress event num=1 x=13 y=15> will be the output where:
        # 1. num=1 is left-click, num=3 is right-click
        # 2. the x,y are the coordinates
        #print("Left Clicked")
        if(self.isMine):
            #print("Game Over")
            self.showMine()
        else:
            if self.getSurroundingMinesTotal == 0:  # if the number of surrounding mines is 0, then we will show all the surrounding cells
                for cell in self.getSurroundingCells:
                    cell.showCell()
            self.showCell()
            # IF WE FINISH THE GAME(num of cells left = num of mines), THEN WE WILL SHOW THE MESSAGE BOX
            if Cell.cellCount == var.mineCount:
                ctypes.windll.user32.MessageBoxW(0, "You Won!", "Game Over", 0)
            
        # WE WILL MAKE THE CELL BUTTON UNCLICKABLE AFTER IT IS CLICKED
        # USING UNBIND METHOD
        self.cell_button.unbind("<Button-1>")
        self.cell_button.unbind("<Button-3>")
        
    def getCell(self,x,y):                      # this will return the cell object at the given coordinates
        for cell in Cell.all:
            if(cell.x == x and cell.y == y):
                return cell
        return None
        
    @property                                   # we made it like an "attribute" so that we can use it like a variable
    def getSurroundingCells(self):
        #print(self.getCell(self.x,self.y))
        surroundedCells = [                     # 8 such possibilities of surrounding cells
            self.getCell(self.x-1,self.y-1),
            self.getCell(self.x-1,self.y),
            self.getCell(self.x-1,self.y+1),
            self.getCell(self.x,self.y-1),
            self.getCell(self.x+1,self.y-1),
            self.getCell(self.x+1,self.y),
            self.getCell(self.x+1,self.y+1),
            self.getCell(self.x,self.y+1),
        ]
        #print(surroundedCells)             # this will print the list of the cells surrounding the clicked cell
        # from this we saw that there are None values in the list, so we will remove them
        surroundedCells = [cell for cell in surroundedCells if cell is not None]    # LIST COMPREHENSION
        #print(surroundedCells)             # removes the None values
        return surroundedCells
        
    @property                                   # made it a "READ-ONLY" attribute
    def getSurroundingMinesTotal(self):         # will get the number of mines surrounding the clicked cell
        counter = 0
        for cell in self.getSurroundingCells:
            if(cell.isMine):
                counter += 1
        return counter
        
    def showCell(self):
        if not self.isOpened:                       # if the cell is already opened, then we will not open it again
            Cell.cellCount -= 1
            #print(self.getSurroundingCells)         # prints the list of surrounding cells
            #print(self.getSurroundingMinesTotal)    # prints the number of mines surrounding the clicked cell
            self.cell_button.configure(text=self.getSurroundingMinesTotal)
        
        # now we will replace/update the label of the number of cells left
            if self.cellCountLabelObject:
                self.cellCountLabelObject.configure(text=f'Cells Left: {Cell.cellCount}')
                # Marks the cell as opened... this will remove the possibility of opening the same cell again
            # If this was a Mine Candidate, then we will remove the yellow color
            self.cell_button.configure(bg="SystemButtonFace")
        self.isOpened = True
        
    def showMine(self):
        # Logic to interrupt the game and display the message of GAME OVER
        self.cell_button.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "You Click On A Mine", "Game Over", 0)    # Generic Message Box
        sys.exit()
        
    def rightClick(self,event):
        #print(event)
        #print("Right Clicked")
        if not self.isMineCandidate:
            self.cell_button.configure(bg="yellow")
            self.isMineCandidate = True
        else:
            self.cell_button.configure(bg="SystemButtonFace")   # we will reset the color to default
            self.isMineCandidate = False
    
    # NOW WE HAVE CREATED ALL THE CELLS... NOW WE WILL CREATE A FUNCTION TO SELECT THE MINES RANDOMLY
    # We have created a static function as it will be used by the class itself(globally) and not by the object(instance)
    
    @staticmethod
    def randomMines():
        mines = random.sample(Cell.all, var.mineCount)      # this will select 5 random cells from the list of all the cells
        for mines in mines:
            mines.isMine = True                 # this will make the isMine attribute of the cell to True
    
    def __repr__(self):                         
        # will basically return an object representation in string format
        # "magic method" which will be called when we do print(Cell.all) and gives the output in the form of Cell(0,0) and so on...
        return f"Cell({self.x},{self.y})"