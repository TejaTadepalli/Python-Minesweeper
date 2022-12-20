from tkinter import *
import variables as var
import functions as func
from button import Cell

# Create the root window ("ROOT" is the name which we are giving by conevention)
root = Tk()

root.geometry(f'{var.width}x{var.height}')          # gives the size of the window (width x height)
root.title("Minesweeper Game")                      # gives the title of the window
root.resizable(False, False)                        # makes the window non-resizable (width, height)
root.configure(bg="black")                          # change the background color of the window

top_frame = Frame(                                  # Creating a frame in the window (using Frame class)
    root,                                           # this "frame" will be present inside root window
    bg = "black",                                   # change the background color of the frame
    width = var.width,                              # width of the frame
    height = func.height_percent(25),                # height of the frame (1/4th of the window)
)

top_frame.place(x=0, y=0)                           # Placement of the frame in the window (x, y)
                                                    # it will start from x=0,y=0 and will go till x=1200,y=150
                                                    # if there was x=20 or smth, it will go from x=20,y=0 to x=1220,y=150

game_title = Label(                                 # Creating a label in the window (using Label class)
    top_frame,                                      # this "label" will be present inside top_frame
    text="Minesweeper",                             # text on the label
    bg="black",                                     # change the background color of the label
    fg="white",                                     # change the foreground color of the label
    font=("Arial", 50, "bold")                      # change the font of the label
)

game_title.place(x=func.width_percent(25), y=30)    # Placement of the label in the window (x, y)

left_frame = Frame(                                 # will be a frame on the left side containing the info
    root,
    bg="black",
    width = func.width_percent(25),                 # one-fourth of the original dimensions
    height = func.height_percent(75)                # will be the reminaing size of the window (3/4th)
)

left_frame.place(x=0, y=func.height_percent(25))    # this will be placed below the top_frame and at 25% of the height

center_frame = Frame(                               # will be a frame in the center containing the game
    root,
    bg="black",
    width = func.width_percent(75),
    height = func.height_percent(75)
)

center_frame.place(x=func.width_percent(25), y=func.height_percent(25))

#button = Button(                                   # Creating a button in the window (using Button class)
#    center_frame,                                  # this "button" will be present inside center_frame
#    bg="blue",
#    text="Click Me",                               # text on the button
#)
#button.place(x=0, y=0)                             # Placement of the button in the window (x, y)

#c1=Cell()
#c1.createButton(center_frame)
# c1.cell_button.place(x=0,y=0) would be the original but as we will face difficulties w/ multiple buttons, we will use grid concept
#c1.cell_button.grid(row=0,column=0)                 # this will place the button in the 0th row and 0th column

#c2=Cell()
#c2.createButton(center_frame)
#c2.cell_button.grid(row=0,column=1)

# as we have multiple buttons, we will use a loop to create the buttons
for x in range(var.gridSize):
    for y in range(var.gridSize):
        C=Cell(x,y)
        C.createButton(center_frame)
        C.cell_button.grid(row=x,column=y)

Cell.cellCountLabel(left_frame)                # will create the label for the cell count
Cell.cellCountLabelObject.place(x=0,y=0)       # will place the label in the left_frame

# print(Cell.all)                                     # will print the list of all the buttons
Cell.randomMines()                                  # will select the mines
#for c in Cell.all:
#    print(c.isMine)                                 # will print the list of all the buttons and whether they are mines or not

root.mainloop()                                     # will tell us that the window is running and to close it we need to click on X button

# The code is basically b/w the root = Tk() and root.mainloop() lines
# For the background color, we can use hex color codes as well...
# we will then try and divide the current box into different sections so as to make the functionality easier
# after creation of buttons, we will try and make them according to "events"... for eg: right-click & left-click are have different uses