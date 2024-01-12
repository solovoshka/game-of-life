# Imports and library implementation
from random import randint
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import colors
import matplotlib.animation as animation
import numpy as np

# LOGIC 
'''
1. A living cell will survive into the next generation by default, unless:
-> it has fewer than two live neighbours (underpopulation).
-> it has more than three live neighbours (overpopulation).

2. A dead cell will spring to life if it has exactly three live neighbours (reproduction).

for this, a cell and a board class is needed (OOP); will need functions such as checking if cell on or off; a function that compares 
cell to neighbors; possible difficulty in making a function that deals with edge cases; will use ani to animate (matplotlib function)
'''


# CLASS CELL
# create a cell class to make many cell objects 
class Cell:
    # attributes a cell can have: a 'dead' (off) or 'alive' (on) status
    def __init__(self):
        self.status = "dead"

    # function sets the cell status to dead 
    def set_dead(self):
        self.status = "dead"
    
    # function sets the cell status to alive 
    def set_alive(self):
        self.status = "alive"
    
    # function that checks if the cell is 'alive' (on) or 'dead'(off) -> boolean 
    def is_alive(self):
        if self.status == "alive":
            return True 
        else: 
            return False
    
    # function that prints the respective character of a cell status (for console use)
    def print_char(self):
        if self.is_alive():
            return "⬛" #  alive
        return "⬜" # dead

# CLASS BOARD  
# create a board class to make a single board with necessary methods         
class Board():
    def __init__(self, rows, columns):
        self.rows = rows # int
        self.columns = columns # int

        # the grid is equal to a 2D array; a cell object is created for each looping of column_cells in the number of columns;
        # the same idea applies for row_cells in the range of number of rows
        # NUMBER OF COLS ITERATES OVER NUMBER OF ROWS; efficient for loop
        self.grid = [[Cell() for column_cells in range(self.columns)] for row_cells in range(self.rows)]
        self.generate_board() # generate the board right away

    # this prints the board (again, for console use)
    def draw_board(self): 
        print('\n'*10)
        print('printing board')
        for row in self.grid:
            for column in row:
                print(column.print_char(), end='')
            print()                             # the essential idea is that insetad of printing everything
                                                # on a new line, to print it by row instead

    # method that randomly chooses value 0 or 1 (because not upper end inclusive) and depending on that val 
    # sets the cell in (row, column) to alive if it is 1
    def generate_board(self):
        for row in self.grid:
            for column in row:
                rannum = randint(0,2)
                if rannum == 1:
                    column.set_alive()

    # function that checks the cells around the given cell 
    # and checks if they are valid/exist (checks for edge cases)  
    #
    # (-1, -1)  (-1, 0)  (-1, 1)   
    # (0, -1)   (0, 0)   (0, 1)
    # (1, -1)   (1, 0)   (1, 1)
    #

    def check_neighbor(self, check_row, check_column): # (check_row, check_column) gives the coordinates for the cell that needs to be checked
        startbound = -1 # this is because ranges are upper end EXCLUSIVE -> so really range (-1, 2) includes -1, -, and 1
        endbound = 2
        # empty list to append neighbors into 
        neighbor_list = []
        # iterate through this supposed 3 x 3 matrix 
        for row in range(startbound, endbound): 
            for column in range(startbound, endbound):

                # the thing that is being checked 
                neighbor_row = check_row + row  # adding the current iteration's values to the specified cell's position 
                neighbor_column = check_column + column # what this is doing, is creating the 3x3 matrix around the cell that needs to be checked
                                                        # hard to explain, but the cell in the grid is not always going to be 0,0 could be any random val
                                                        # in a sense, makes the matrix in terms of the given cell (if makes sense)
                # existing condition
                valid_neighbor = True

                if (neighbor_row) == check_row and (neighbor_column) == check_column: # this checks if the cell is equal to the center cell,
                    valid_neighbor = False                                        # which is the cell being checked!!

                if (neighbor_row) < 0 or (neighbor_row) >= self.rows:   # if the row being checked is less than zero or greater than 
                    valid_neighbor = False                         # the total amount of rows, then it is not a valid neighbor to be checked

                if (neighbor_column) < 0 or (neighbor_column) >= self.columns: # same with the columns 
                    valid_neighbor = False  #FIGURE OUT EQUALITY SIGNS 

                if valid_neighbor: # if the cell passed all the previous tests (if it exists)
                    neighbor_list.append(self.grid[neighbor_row][neighbor_column]) #gets added into the neighbor list that I will then use to check
        return neighbor_list # returns a list of all the existing neighbors, so really its either 8, 5, or 3 valid neighbors
    
    # function that uses the known nieghbors and determines the cells status for the next generation as well as updates them 
    def update_board(self):
        print ("updating board ...")
        the_alive = []
        the_dead = [] 
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                check_neighbor = self.check_neighbor(row, column)                
                
                living_neighbors_count = []
                for neighbor in check_neighbor:
                    if neighbor.is_alive():
                        living_neighbors_count.append(neighbor)

                cell = self.grid[row][column]
                stat_main_cell = cell.is_alive()

                # check the cases for when the cell to be checked is alive 
                if cell.is_alive():
                    if len(living_neighbors_count) < 2 or len(living_neighbors_count) > 3: #basically, if the amount of alive neighbors is less than 2 (underpop)
                        the_dead.append(cell)                                              #or more than 3 (overpop), the cell dies and appends to deadlist

                    if len(living_neighbors_count) == 2 or len(living_neighbors_count) == 3:
                        the_alive.append(cell)

                else: # if the cell being checked is dead 
                    if len(living_neighbors_count) == 3:
                        the_alive.append(cell)
        
        # set cell statuses: for all the cells in the alive list, set them alive; for all the cells in the dead list, set them dead            
        for items in the_alive:
            items.set_alive()
        for items in the_dead:
            items.set_dead()

# VISUAL: function update for use with matplotlib animation
def update(frame, gol_board, ax, cmap):

    # calls already made update_board function from Board class
    gol_board.update_board()
    ax.clear()
    ax.set_title(f'Generation: {frame + 1}')

    # matplot syntax for the data 
    grid_data = np.zeros((gol_board.rows, gol_board.columns))
    for row in range(gol_board.rows):
        for col in range(gol_board.columns):
            grid_data[row, col] = 1 if gol_board.grid[row][col].is_alive() else 0

    ax.imshow(grid_data, cmap=cmap)

    ax.grid(True, linestyle="-", color='black', linewidth=1)
    ax.set_xticks([])
    ax.set_yticks([])

# MAIN IMPLEMENTATION
def main():

# prints
    print("Hello! Welcome to Conway's Game of Life!")
    print("The Game of Life is a single user cellular automaton, where small cells")
    print("aim to replicate tiny live organism cells. The rules are very simple:")
    print("")
    print("-> if a cell has less than two neighbors:")
    print("   it dies from underpopulation (turns off)")
    print("-> if a cell has more than three neighbors:")
    print("   it dies from overpopulation (turns off)")
    print("-> if a cell has two or three neighbors:")
    print("   it remains alive (on)")
    print("-> exactly three neighbors makes it come alive (turns on)")
    print("                         enjoy :)!")
    print("")
    print("Please input how many rows, columns, and generations you would like in your game. \nKeep this integer in the range (1,200) inclusive.")
    print("The input will create a board with dimensions (rows, columns) and will iterate [generation] amount of times.")
# Main Implementation
    
    # user input; checks if input value is an integer within the range 
    while True:
        try:
            user_rows = int(input("How many rows?"))
            if 0 < user_rows <= 200:
                break
            else:
                print("Please enter a number in the range 1 to 200. Try again.")
        except ValueError:
            print("Please enter a valid integer. Try again.")

    while True:
        try:
            user_columns = int(input("How many columns?"))
            if 0 <= user_columns <= 200:
                break
            else:
                print("Please enter a number in the range 1 to 200. Try again.")
        except ValueError:
            print("Please enter a valid integer. Try again.")

    while True:
        try:
            num_frames = int(input("How many generations?"))
            if 0 <= num_frames <= 200:
                break
            else:
                print("Please enter a number in the range 1 to 200. Try again.")
        except ValueError:
            print("Please enter a valid integer. Try again.")


    # create a figure and initialize board 
    fig, ax = plt.subplots()
    gol_board = Board(user_rows, user_columns)

    # personalize color map for squares * white will correspond to cells with value 0 (off) and teal to cells with value 1 (on)
    cmap = colors.ListedColormap(['white', 'teal'])

    # this is responsible for animating my figure; takes parameters figure, update function; fargs responsible for paramaters of update 
    # function; frames, which is determined by user (and then ani executes according to this number); interval controls how fast 
    # the animation happens; and I am still figuring out repeat 
    ani = animation.FuncAnimation(fig, update, fargs=(gol_board, ax, cmap), frames=num_frames, interval=500, repeat=False)
    plt.show()

main()


