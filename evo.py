import random
import pygame
from pygame.locals import *

class Food():    
    
    def __init__(self, x, y, screen, colour = (0, 255, 0),size = 2):
        self.x = int(x)
        self.y = int(y)
        self.screen = screen
        self.colour = colour
        self.size = size

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, [int(self.x), int(self.y)], self.size)


gen = {'speed': 30, 'maxenergy': 1000, 'mutationrate': 0.5, 'mutationvalue': 0.2,'increasemutationrate':0.5, 'sensepower': 5, 'size': 7}
class Animal():
    def __init__(self, x, y, gen, fps, screen, screensize, colour = (0, 0, 255)):
        self.x = x
        self.xdir = 0
        self.y = y
        self.ydir = 10
        self.gen = gen
        self.fps = fps
        self.screen = screen
        self.size = gen['size']
        self.colour = colour
        self.screensize = screensize
        self.maxenergy = gen['maxenergy']
        self.speed = gen['speed']
        self.energy = self.maxenergy//2
        self.sensepower = gen['sensepower'] * self.size


    def draw(self):
        pygame.draw.circle(self.screen, self.colour, [int(self.x), int(self.y)], self.size)
        pygame.draw.circle(self.screen, (0,0,0), [int(self.x + self.xdir), int(self.y+self.ydir)], 1)


    def move(self):
        self.x += self.xdir / self.fps * self.speed
        self.y += self.ydir / self.fps * self.speed
        self.energy -= self.speed * 5 / self.fps

    def boundaries(self):
        if self.x + self.size> self.screensize[0]:
            self.x = self.screensize[0] - self.size
        if self.x < self.size:
            self.x = self.size
        if self.y + self.size> self.screensize[1]:
            self.y = self.screensize[1] - self.size
        if self.y < self.size:
            self.y = self.size

    def death(self):
        newfood = []
        for i in range(int(self.maxenergy / 10)):
            food = (makefood([self.size,self.size], screen))
            food.x+=self.x
            food.y+=self.y
            newfood.append(food)
        return newfood



    def eat(self, arr):
        eaten = []
        for i in range(len(arr)-1, -1, -1):
            if dist(self, arr[i])<self.size + arr[i].size:
                eaten.append(i)
                self.energy +=50
        for k in eaten:
            arr.pop(k)

    def sensefood(self, farr):
        list = []
        for i in farr:
            if dist(self, i)<= self.sensepower:
                list.append(i)
        x = 0
        y = 0
        for k in list:
            skvdist = dist(self, k)**2
            x+= (k.x - self.x)/skvdist
            y+= (k.y - self.y)/skvdist

        return [x, y]

    def turn(self, farr):
        dir = self.sensefood(farr)
        a = ((dir[0] ** 2 + dir[1] ** 2) / 100) ** 0.5
        if a!=0:
            self.xdir = dir[0] / a
            self.ydir = dir[1] / a

    def breed(self):
        genom = {}
        for a in gen.values():
            if a!= 'mutationrate' and a!= 'increasemutationrate':
                if random.random()< gen['mutationrate']:
                    if random.random()<gen['increasemutationrate']:
                        genom[a] = gen[a] * (1 + gen['mutationvalue'])
                    else:
                        genom[a] = gen[a] * (1 - gen['mutationvalue'])
            elif a == 'mutationrate':
                if random.random()< gen['mutationrate']:
                    if random.random()< gen['increasemutationvalue']:
                        genom[a] = gen[a] * (1+gen['mutationrate']) / (gen[a] * (1+gen['mutationrate']) + 1 - gen['mutationrate'] )
                    else:
                        genom[a] = gen[a] * (1 - gen['mutationrate']) / (gen[a] * (1 + gen['mutationrate']) + 1 - gen['mutationrate'])




        animal = Animal(self.x + 2 * self.size, self.y + 2 * self.size, genom, fps, screen, screensize, colour = (0, 0, 255))

    # Execute animal actions on next move
    def total(self, farr, aarr):
        self.turn(farr)
        self.move()
        self.boundaries()
        eaten = self.eat(farr)
        self.draw()


def makefood(size, screen):
    return Food(random.randint(1, size[0] - 1), random.randint(1, size[1] - 1), screen)

def dist(a, b):
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

def checkdeath(aarr):
    nf = []
    deathlist = []
    for i in range(len(aarr)):
        if aarr[i].energy<=0:
            deathlist.append(i)
            
    for k in range(len(deathlist)):
        flist = (aarr.pop(deathlist[k])).death()
        nf+=flist
    return nf


if __name__ == "__main__":
    screensize = (1280, 640)
    fps = 100
    pygame.init()
    screen = pygame.display.set_mode(screensize)
    clock = pygame.time.Clock()
    done = False

    # food array
    farr = []

    # animal array
    aarr = []

    timer = 0
    aarr.append(Animal(860, 320, gen, fps, screen, screensize))

    black = (0, 0, 0)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.display.flip()
                done = True

        if timer % int(fps / 100) == 0:
            farr.append(makefood(screensize, screen))

        timer += 1

        farr += checkdeath(aarr)
        for i in aarr:
            print(i.energy)
            i.total(farr, aarr)

        for i in farr:
            i.draw()

        pygame.display.flip()
        screen.fill(black)
        clock.tick(fps)

    pygame.quit()
