### to sort out
# leaderboard
# touching more than one circle simultaneously
# code clean up

import math
import random
import time
import Tkinter as tk

class gamecircle:
    EATER = 0
    FOOD = 1
    HUMAN = 0
    MACHINE = 1
    STARTMASS = 20
    def __init__(self,position,speed,type,controller,colour,name):
        self.position = position
        self.speed = speed
        self.type = type
        self.controller = controller
        self.colour = colour
        if controller == self.EATER:
            self.mass = gamecircle.STARTMASS
        else:
            self.mass = random.randint(2,15)
        self.alive = True
        self.setradius()
        self.maxspeed = 0
        self.setmaxspeed()
        self.name = name

    def growby(self, addedmass):
        self.mass += addedmass
        self.setradius()
        self.setmaxspeed()

    def setradius(self):
        self.radius = math.sqrt(self.mass)

    def setmaxspeed(self):
        #print('setting max speed: {} {} {}'.format(self.maxspeed, self.radius, 4.0/math.sqrt(self.radius)))
        self.maxspeed = 4 / self.radius ** (1.0/2.5)
        #print(self.maxspeed)

    def movestep(self, width, height):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.speed[0] = 0
        if self.position[0] + self.radius > width:
            self.position[0] = width - self.radius
            self.speed[0] = 0
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.speed[1] = 0
        if self.position[1] + self.radius > height:
            self.position[1] = height - self.radius
            self.speed[1] = 0

    def normalise_speed(self):
        abs_speed = math.sqrt((self.speed[0])**2 + (self.speed[1])**2)
        #print("abs_speed: {}, maxspeed: {} radius: {}".format(abs_speed,self.maxspeed,self.radius))
        if abs_speed > self.maxspeed:
            for i in range(2):
                self.speed[i] = self.speed[i]/abs_speed*self.maxspeed



class board:
    def __init__(self,width,height,startingfoods):
        self.bot_counter = 1
        self.human_counter = 1
        self.width = width
        self.height = height
        self.foods = []
        self.eaters=[]
        self.populate(startingfoods)


    def populate(self,numberoffoods):
        for num in range(numberoffoods):
            self.add_food()

        for i in range(7):
            self.add_eater(gamecircle.MACHINE)

    def add_food(self):
        pos = [random.uniform(0,self.width),random.uniform(0,self.height)]
        gc = gamecircle(pos,[0,0],gamecircle.FOOD,gamecircle.MACHINE,'green',name='food')
        self.foods.append(gc)

    def add_eater(self,controller):
        pos = [random.uniform(0,self.width),random.uniform(0,self.height)]
        if controller == gamecircle.HUMAN:
            gc = gamecircle(pos,[0,0],gamecircle.EATER,controller,'red', name = "Me_"+str(self.human_counter))
            self.human_counter += 1
            self.mainplayer = gc
        else:
            gc = gamecircle(pos,[0,0],gamecircle.EATER,controller,'blue',name="Bot_"+str(self.bot_counter))
            self.bot_counter += 1
        self.eaters.append(gc)

    def update(self):
        for gc in self.eaters:
            if gc.controller != gamecircle.HUMAN:
                self.get_move(gc)
            gc.movestep(self.width, self.height)
        self.collision_detction()
        self.retire_food()

    def retire_food(self):
        x = random.randint(1,20)
        if x == 1:
            self.foods.pop(0)
            self.add_food()

    def get_move(self, gc):
        move = random.randint(1,random.randint(4,100))
        if move == 1:
            gc.speed[0] -= gc.maxspeed / 5
        elif move == 2:
            gc.speed[0] += gc.maxspeed / 5
        elif move == 3:
            gc.speed[1] -= gc.maxspeed / 5
        elif move == 4:
            gc.speed[1] += gc.maxspeed / 5
        gc.normalise_speed()

    def collision_detction(self):
        for player in self.eaters:
            for food in self.foods:
                distance_apart = math.sqrt((player.position[0] - food.position[0])**2 + (player.position[1] - food.position[1])**2)
                max_eating_distance = player.radius + food.radius
                if distance_apart < max_eating_distance:
                    self.consume_food(player, food)
        p1s = []
        p2s = []
        for i in range(len(self.eaters)):
            for j in range(i):
                player_1 = self.eaters[i]
                player_2 = self.eaters[j]
                distance_apart = math.sqrt((player_1.position[0] - player_2.position[0])**2 + (player_1.position[1] - player_2.position[1])**2)
                max_eating_distance = player_1.radius + player_2.radius
                if distance_apart < max_eating_distance:
                    p1s.append(player_1)
                    p2s.append(player_2)
        for i in range(len(p1s)):
            self.player_collision(p1s[i], p2s[i])

    def player_collision(self,p1,p2):
        buffer_mass = 20
        if p1.mass > p2.mass + buffer_mass:
            self.consume_player(p1,p2)
        elif p2.mass > p1.mass + buffer_mass:
            self.consume_player(p2,p1)

    def consume_player(self, eater, food):
        eater.growby(food.mass)
        self.eaters.remove(food)
        controller = food.controller
        self.add_eater(controller)

    def consume_food(self, player, food):
        player.growby(food.mass)
        self.foods.remove(food)
        self.add_food()

    def draw(self):
        global canvas
        canvas.delete('all')
        self.visible_x = self.mainplayer.radius * 3 + 100
        self.visible_y = self.mainplayer.radius * 3 + 100
        canvas.create_rectangle(0,0,self.width, self.height, fill = 'grey', outline = 'grey')
        self.draw_level()
        #canvas.create_rectangle(-10,-10, self.width+10,self.height+10,fill='grey')
        #canvas.create_rectangle(self.mainplayer.position[0] - self.visible_x,self.mainplayer.position[1] - self.visible_y, self.mainplayer.position[0] + self.visible_x,self.mainplayer.position[1] + self.visible_y,fill='white',outline='grey')
        for gc in self.eaters:
            if self.in_view(gc):
                self.draw_gc(gc)
        for gc in self.foods:
            if self.in_view(gc):
                self.draw_gc(gc)
        self.draw_leaderboard()
        txt = "Mass: {}\nPos_x: {:.1f}\nPos_y: {:.1f}\nSpeed_x: {:.1f}\nSpeed_y: {:.1f}".format(self.mainplayer.mass, self.mainplayer.position[0],self.mainplayer.position[1],self.mainplayer.speed[0],self.mainplayer.speed[1])
        canvas.create_text(500 - 50, 50, fill ='red', text = txt)

    def draw_leaderboard(self):
        global canvas
        self.eaters.sort(key=lambda x: x.mass, reverse=True)
        txt = ''
        for i in range(5):
            txt += self.eaters[i].name + '   ' + str(self.eaters[i].mass) + '\n'
        canvas.create_text(50,50,fill = 'red', text = txt)

    def in_view(self,gc):
        in_view_in_x = abs(gc.position[0] - self.mainplayer.position[0]) < self.visible_x + gc.radius
        in_view_in_y = abs(gc.position[1] - self.mainplayer.position[1]) < self.visible_y + gc.radius
        return in_view_in_x and in_view_in_y

    def addmainplayer(self):
        self.mainplayer = gamecircle(position=[self.width/2,self.height/2],speed=[0,0],type=gamecircle.EATER,controller=gamecircle.HUMAN,colour='red',name="Me_"+str(self.human_counter))
        self.human_counter += 1
        self.eaters.append(self.mainplayer)

    def draw_gc(self,gc):
        global canvas
        rel_centre_x = gc.position[0] - self.mainplayer.position[0]
        rel_centre_y = gc.position[1] - self.mainplayer.position[1]
        in_view_x = (rel_centre_x / self.visible_x) * 500 + 250
        in_view_y = (rel_centre_y / self.visible_y) * 500 + 250
        canvas.create_oval(in_view_x - gc.radius/self.visible_x * 500,in_view_y - gc.radius/self.visible_y * 500,in_view_x + gc.radius/self.visible_x * 500,in_view_y + gc.radius/self.visible_y * 500,fill=gc.colour)
        if gc.speed[0] != 0 or gc.speed[1] !=0:
            canvas.create_line(in_view_x, in_view_y, in_view_x + gc.speed[0]/gc.maxspeed*50,in_view_y + gc.speed[1]/gc.maxspeed*50, arrow=tk.LAST)

    def draw_level(self):
        rel_centre_x = self.width/2 - self.mainplayer.position[0]
        rel_centre_y = self.height/2 - self.mainplayer.position[1]
        in_view_x = (rel_centre_x / self.visible_x) * 500 + 250
        in_view_y = (rel_centre_y / self.visible_y) * 500 + 255
        width = self.width / self.visible_x * 500
        height = self.height / self.visible_y * 500
        canvas.create_rectangle(in_view_x - width/2, in_view_y - height/2,in_view_x + width/2,in_view_y + height/2,fill='white')

def key_pressed(event):
    #print('key')
    if event.char == 'a':
        gb.mainplayer.speed[0] -= gb.mainplayer.maxspeed / 5
    elif event.char == 'd':
        gb.mainplayer.speed[0] += gb.mainplayer.maxspeed / 5
    elif event.char == 'w':
        gb.mainplayer.speed[1] -= gb.mainplayer.maxspeed / 5
    elif event.char == 's':
        gb.mainplayer.speed[1] += gb.mainplayer.maxspeed / 5
    gb.mainplayer.normalise_speed()

gb = board(500,250,100)
gb.addmainplayer()





root=tk.Tk()

canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()
root.bind("<Key>", key_pressed)
root.title("Game")
counter = 0
while gb.mainplayer.alive:
    gb.update()
    gb.draw()
    root.update()


root.mainloop()
