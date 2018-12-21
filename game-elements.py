import math
import random
import time
import Tkinter as tk

class gamecircle:
    EATER = 0
    FOOD = 1

    HUMAN = 0
    MACHINE = 1

    STARTMASS = 5
    STARTMAXSPEED = 1

    def __init__(self,position,speed,type,controller,colour):
        self.position = position
        self.speed = speed
        self.type = type
        self.controller = controller
        self.colour = colour
        if controller == self.EATER:
            self.mass = gamecircle.STARTMASS
        else:
            self.mass = random.randint(2,15)
        self.maxspeed = gamecircle.STARTMAXSPEED
        self.alive = True
        self.setradius()

    def growby(self, addedmass):
        self.mass += addedmass
        updateradius()

    def setradius(self):
        self.radius = math.sqrt(self.mass)

    def movestep(self):
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]

    def draw(self):
        global canvas
        x1 = self.position[0] - self.radius
        y1 = self.position[1] - self.radius
        canvas.create_oval(x1,y1,x1+2*self.radius,y1+2*self.radius,fill=self.colour)


class board:
    def __init__(self,width,height,startingfoods):
        self.width = width
        self.height = height
        self.foods = []
        self.eaters=[]
        self.populate(startingfoods)

    def populate(self,numberoffoods):
        for num in range(numberoffoods):
            self.add_food()

    def add_food(self):
        pos = [random.uniform(0,self.width),random.uniform(0,self.height)]
        gc = gamecircle(pos,[0,0],gamecircle.FOOD,gamecircle.MACHINE,'green')
        self.foods.append(gc)


    def update(self):
        for gc in self.eaters:
            gc.movestep()
        self.collision_detction()

    def collision_detction(self):
        for player in self.eaters:
            for food in self.foods:
                distance_apart = math.sqrt((player.position[0] - food.position[0])**2 + (player.position[1] - food.position[1])**2)
                max_eating_distance = player.radius + food.radius
                if distance_apart < max_eating_distance:
                    self.consume(player, food)

    def consume(self, player, food):
        player.mass += food.mass
        player.setradius()
        self.foods.remove(food)
        self.add_food()


    def draw(self):
        global canvas
        canvas.delete('all')
        self.visible_x = self.mainplayer.radius * 10
        self.visible_y = self.mainplayer.radius * 6
        canvas.create_rectangle(-10,-10, self.width+10,self.height+10,fill='grey')
        canvas.create_rectangle(self.mainplayer.position[0] - self.visible_x,self.mainplayer.position[1] - self.visible_y, self.mainplayer.position[0] + self.visible_x,self.mainplayer.position[1] + self.visible_y,fill='white',outline='grey')
        for gc in self.eaters:
            if self.in_view(gc):
                gc.draw()
        for gc in self.foods:
            if self.in_view(gc):
                gc.draw()
        txt = "Mass: {}\nPos_x: {}\nPos_y: {}".format(self.mainplayer.mass, self.mainplayer.position[0],self.mainplayer.position[1])
        canvas.create_text(self.width - 50, 50, fill ='red', text = txt)


    def in_view(self,gc):
        in_view_in_x = abs(gc.position[0] - self.mainplayer.position[0]) < self.visible_x
        in_view_in_y = abs(gc.position[1] - self.mainplayer.position[1]) < self.visible_y
        return in_view_in_x and in_view_in_y

    def addmainplayer(self):
        self.mainplayer = gamecircle(position=[self.width/2,self.height/2],speed=[2,0],type=gamecircle.EATER,controller=gamecircle.HUMAN,colour='black')
        self.eaters.append(self.mainplayer)


SPEED_CHANGE = 1


def key_pressed(event):
    global player
    print('key')
    if event.char == 'a':
        gb.mainplayer.speed[0] -= SPEED_CHANGE
    elif event.char == 'd':
        gb.mainplayer.speed[0] += SPEED_CHANGE
    elif event.char == 'w':
        gb.mainplayer.speed[1]-= SPEED_CHANGE
    elif event.char == 's':
        gb.mainplayer.speed[1] += SPEED_CHANGE

gb = board(500,250,50)
gb.addmainplayer()





root=tk.Tk()

canvas = tk.Canvas(root, width=500, height=250)
canvas.pack()
root.bind("<Key>", key_pressed)
root.title("Game")
counter = 0
while gb.mainplayer.alive:
    gb.update()
    gb.draw()
    root.update()


root.mainloop()
