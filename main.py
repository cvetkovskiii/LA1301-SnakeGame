import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class box(object):
    rows = 20
    w = 500

    def __init__(self, start, directionX=1, directionY=0, color=(0,255, 0)):
        self.pos = start
        self.directionX = 1
        self.directionY = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.directionX = dirnx
        self.directionY = dirny
        self.pos = (self.pos[0] + self.directionX, self.pos[1] + self.directionY)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        e = self.pos[0]
        b = self.pos[1]

        pygame.draw.rect(surface, self.color, (e * dis + 1, b * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (e * dis + centre - radius, b * dis + 8)
            circleMiddle2 = (e * dis + dis - radius * 2, b * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = box(pos)
        self.body.append(self.head)
        self.directionX = 0
        self.directionY = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.directionX = -1
                    self.directionY = 0
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                elif keys[pygame.K_RIGHT]:
                    self.directionX = 1
                    self.directionY = 0
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                elif keys[pygame.K_UP]:
                    self.directionX = 0
                    self.directionY = -1
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

                elif keys[pygame.K_DOWN]:
                    self.directionX = 0
                    self.directionY = 1
                    self.turns[self.head.pos[:]] = [self.directionX, self.directionY]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.directionX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.directionX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.directionY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.directionY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.directionX, c.directionY)



    def addBox(self):
        tail = self.body[-1]
        dx, dy = tail.directionX, tail.directionY

        if dx == 1 and dy == 0:
            self.body.append(box((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(box((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(box((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(box((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].directionX = dx
        self.body[-1].directionY = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def DrawAgainInWindow(surface):
    global rows, width, s, food
    surface.fill((0, 0, 0))
    s.draw(surface)
    food.draw(surface)
    pygame.display.update()


def ChoosingRandomPositionforSnacks(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():

    global width, rows, s, food
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    food = box(ChoosingRandomPositionforSnacks(rows, s), color=(238, 130, 238))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == food.pos:
            s.addBox()
            food = box(ChoosingRandomPositionforSnacks(rows, s), color=(238, 130, 238))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('Unfortunaley You lost! Play again ? [Okay].')
                s.setToDefault((10, 10))
                break

        DrawAgainInWindow(win)

    pass


main()


