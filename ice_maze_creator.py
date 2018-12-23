import numpy as np
import Tkinter as tk
import math
import os

BOARD_SIZE = 400
LEVEL_SIZE = 9
CELL_WIDTH = 20
CELL_HEIGHT = 20
BUFFER = 40
WINDOW_WIDTH = BOARD_SIZE+2*BUFFER
WINDOW_HEIGHT = WINDOW_WIDTH + 200

PLAYER_COLOUR = 'green'
EMPTY_COLOUR = 'white'
OUT_OF_BOUNDS_COLOUR = 'black'
GOAL_COLOUR = 'red'
UP = 'up' #denotes vertical block
HORIZONTAL = 'horizontal' #denotes block on side, pointing along x
VERTICAL = 'vertical' #denotes block on side, pointing along x

goal_x = LEVEL_SIZE - 1
goal_y = LEVEL_SIZE - 1
start_x = 0
start_y = 0
gridx = 0
gridy = 0


player_state = UP
player_x = start_x
player_y = start_y


grid = np.zeros((LEVEL_SIZE,LEVEL_SIZE))
grid.fill(2)
grid[0][0] = 0
grid[0][LEVEL_SIZE-1] = 3

def draw_game():
    global grid, canvas
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x = BUFFER + j * CELL_WIDTH
            y = BUFFER + i * CELL_HEIGHT
            if grid[i][j] == 1:
                colour = 'black'
            elif grid[i][j] == 0:
                colour = 'blue'
            elif grid[i][j] == 2:
                colour = 'cyan'
            elif grid[i][j] == 3:
                colour = 'red'
            canvas.create_rectangle(x,y,x+CELL_WIDTH,y+CELL_HEIGHT, fill=colour)


def inboard(x,y):
    x = x - BUFFER
    y = y - BUFFER
    return (x >=0 and x < LEVEL_SIZE * CELL_WIDTH and y >=0 and y < LEVEL_SIZE * CELL_HEIGHT)

def select(event):
    global grid, gridx, gridy
    x = event.x
    y = event.y
    if inboard(x,y):
        gridx = math.floor((x - BUFFER) / CELL_WIDTH)
        gridy = math.floor((y - BUFFER) / CELL_HEIGHT)
        if grid[gridy][gridx] == 2:
            grid[gridy][gridx] = 1
        elif grid[gridy][gridx] == 1:
            grid[gridy][gridx] = 2
        draw_game()



def print_level():
    global grid
    print(np.array2string(grid, separator=', '))




if __name__ == '__main__':

    root=tk.Tk()
    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    canvas.pack()
    root.bind("<Button-1>", select)
    draw_game()

    b = tk.Button(root, text='Save',command=print_level)
    b.pack()

    root.mainloop()
