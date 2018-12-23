import Tkinter as tk
import time
import math
import random



#game fucntions needed for ai:
# give current state
# give available actions
# make a move
# evaluate reward
# draw itself
# provide: , possible moves for each state


class ice_maze_game:
    START = 0
    HOLE = 1
    ICE = 2
    END = 3
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    move_reverse_dict = {LEFT:'left', RIGHT:'right', UP:'up', DOWN:'down'}
    color_dict = {START:'blue', HOLE:'black', ICE:'cyan', END:'red'}
    reward_dict = {START:-1, ICE:-1, HOLE: -100, END: 100}
    SQUARE_SIZE = 50
    BUFFER_SIZE = 20
    def __init__(self):
        # [ start : hole : ice : ice
        #   ice   : ice  : hole: ice
        #   ice   : ice  : ice : ice
        #   hole  : ice  : end : ice ]
        # self.map = [
        #          [self.START, self.HOLE, self.ICE,  self.ICE],
        #          [self.ICE,   self.ICE,  self.HOLE, self.ICE],
        #          [self.ICE,   self.ICE,  self.ICE,  self.ICE],
        #          [self.HOLE,  self.ICE,  self.END,  self.ICE]
        #          ]
        # self.map = [[0,2,1,2,3],
        #             [1,2,1,2,1],
        #             [2,2,1,2,2],
        #             [2,1,1,1,2],
        #             [2,2,2,2,2]]
        self.map =  [[ 0.,  2.,  2.,  2.,  2.,  2.,  2.,  1.,  3.],
 [ 2.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  2.],
 [ 2.,  2.,  2.,  2.,  2.,  2.,  2.,  1.,  2.],
 [ 2.,  1.,  1.,  2.,  2.,  2.,  2.,  1.,  2.],
 [ 2.,  2.,  2.,  2.,  1.,  2.,  2.,  1.,  2.],
 [ 1.,  1.,  1.,  2.,  2.,  1.,  2.,  1.,  2.],
 [ 2.,  2.,  2.,  2.,  2.,  1.,  1.,  1.,  2.],
 [ 2.,  2.,  1.,  1.,  1.,  1.,  1.,  1.,  2.],
 [ 2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.]]
        self.number_of_possible_states = len(self.map) * len(self.map[0])
        self.number_of_possible_actions = 4
        self.possible_actions_for_ = []
        for j in range(self.number_of_possible_states):
            self.possible_actions_for_.append(self.get_allowed_actions_for_state_(j))
        self.root=tk.Tk()
        self.root.title('board')
        width = self.SQUARE_SIZE * len(self.map[0]) + 2 * self.BUFFER_SIZE
        height = self.SQUARE_SIZE * len(self.map) + 2 * self.BUFFER_SIZE
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.rendering = True
        self.reset()
        self.draw_board()
        self.draw_player()

    def do_action(self,direction):
        self.action_made = direction
        self.moved_from_state_number = self.player_position_to_state_number()
        self.move_player(direction)
        self.current_state_number = self.player_position_to_state_number()
        self.current_reward = self.get_current_reward()
        self.draw_player()

    def episode_ongoing(self):
        if abs(self.current_reward) == 100:
            self.player_alive = False
        return self.player_alive

    def get_allowed_actions_for_state_(self,state_number):
        position = self.state_number_to_player_position(state_number)
        possible_actions = [i for i in range(self.number_of_possible_actions)]
        if position['x'] == 0:
            possible_actions.remove(self.LEFT)
        elif position['x'] == len(self.map[0]) - 1:
            possible_actions.remove(self.RIGHT)
        if position['y'] == 0:
            possible_actions.remove(self.UP)
        elif position['y'] == len(self.map) - 1:
            possible_actions.remove(self.DOWN)
        txt = 'allowed_moves: '
        return possible_actions

    def state_number_to_player_position(self,number):
        x = number % len(self.map[0])
        y = math.floor(number / len(self.map))
        return {'x':x, 'y':y}

    def move_player(self,direction):
        if direction == self.LEFT:
            self.player_position['x'] -= 1
        elif direction == self.RIGHT:
            self.player_position['x'] += 1
        elif direction == self.UP:
            self.player_position['y'] -= 1
        elif direction == self.DOWN:
            self.player_position['y'] += 1

    def player_position_to_state_number(self):
        num = 0
        num += self.player_position['x']
        num += self.player_position['y'] * len(self.map[0])
        return num

    def reset(self):
        self.player_position = {'x':0 , 'y':0}
        self.current_state_number  = self.player_position_to_state_number()
        self.draw_player()
        self.player_alive = True
        self.current_reward = -1

    def get_current_reward(self):
        x = self.player_position['x']
        y = self.player_position['y']
        tile_type = self.map[y][x]
        return self.reward_dict[tile_type]

    def draw_board(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                color = self.color_dict[self.map[row][col]]
                x = self.BUFFER_SIZE + col * self.SQUARE_SIZE
                y = self.BUFFER_SIZE + row * self.SQUARE_SIZE
                self.canvas.create_rectangle(x,y,x+self.SQUARE_SIZE,y+self.SQUARE_SIZE,fill=color)
        self.root.update()

    def draw_player(self):
        if self.rendering:
            try:
                self.canvas.delete(self.player_circle)
            except:
                pass
            x = self.BUFFER_SIZE + self.player_position['x'] * self.SQUARE_SIZE
            y = self.BUFFER_SIZE + self.player_position['y'] * self.SQUARE_SIZE
            self.player_circle = self.canvas.create_oval(x,y,x+self.SQUARE_SIZE,y+self.SQUARE_SIZE,fill='white')
            self.root.update()
