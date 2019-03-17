# Machine Learning Code writen by Liam Smith
# Some computers cannot handle a large amount of dots.
# Change the number of dots through the DOTS variable
# NOTE The number of dots changes throughout the game
# At generation 15, and 50, the number of dots decreases.
import pygame
import random
import math
pygame.init()
disp = pygame.display
win = disp.set_mode((500,500))
DELAY = 3
generation = 1
gx = 250
gy = 50
running = True
MUTATIONS = 200
DOTS = 1000
v = 5
moves = 850
dots = {}
for i in range(DOTS):
    turns = []
    for p in range(moves):
        turns.append(random.randint(0, 359))
    dots[i] = [True, 250, 450, turns, False]
rank = []
pos = 0
king = ''
time = 0
def create(fittest):
    dots = {}
    global time
    time = 0
    global generation
    generation += 1
    global king
    king = fittest[0]
    dots[0] = [True, 250, 450, king[2], False]
    for i in range(1, DOTS):
        frank = []
        for z in range(0, len(fittest[i%10][2])):
            frank.append(fittest[i%10][2][z])
        dots[i] = [True, 250, 450, mutate(frank), False]
    return dots


def mutate(quack):
    flip = []
    for i in range(moves):
        flip.append(quack[i])
    for i in range(MUTATIONS):
        f = random.randint(2, moves-2)
        flip[f] = random.randint(0, 359)
    return flip

def ranking(x, y, timer, alive):
    life = 1000
    if alive or timer:
        life = 1
    if timer:
        return int((((gx-x)**2+(gy-y)**2))*(0.1*timer))
    else:
        return int((((gx-x)**2+(gy-y)**2)**0.5)*(25500)*life)
while running:
    if pygame.key.get_pressed()[pygame.K_UP]:
        DELAY += 1
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        DELAY -= 1
        if DELAY < 0:
            DELAY = 0
    if generation >= 15:
        MUTATIONS = 100
        DOTS = 200
    if generation > 50:
        MUTATIONS = 50
        DOTS = 100
    if generation > 100:
        MUTATIONS = 30
    if generation > 150:
        MUTATIONS = 20
    if generation > 200:
        MUTATIONS = 10
    if generation > 300:
        MUTATIONS = 5
    if generation > 400:
        MUTATIONS = 1
    disp.set_caption("Generation {}".format(generation))
    pygame.time.delay(DELAY)
    time += 3
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (255, 0, 0), (gx,gy, 15, 15))
    pygame.draw.rect(win, (0, 0, 0), (125, 200, 250, 15))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for dot in dots:
        if pos == moves-1:
            stats[0] = False
            c = (0, 255, 255)
        stats = dots[dot]
        if stats[0] == True:
            cx = stats[1]
            cy = stats[2]
            if cx >= 250 and cy >=50 and cx <= 265 and cy <= 65:
                stats[0] = False
                stats[4] = time
            elif (cx >= 485 or cx <=0 or cy >= 485 or cx <= 0) or (cx >= 125 and cx <= 375 and cy >= 200 and cy <= 215):
                stats[0] = False
            else:
                c = (0, 0, 0)
                if dot == 0:
                    c = (0, 255, 0)
                k = stats[3][pos]
                stats[1] += int(math.sin(k*(math.pi/180))*v)
                stats[2] -= int(math.cos(k*(math.pi/180))*v)
        pygame.draw.rect(win, c, (stats[1], stats[2], 6, 6))
        dots[dot] = stats
    pos += 1
    if pos == moves:
        for dot in dots:
            rank.append([ranking(dots[dot][1], dots[dot][2], dots[dot][4], dots[dot][0]), dot, dots[dot][3]])
        rank = sorted(rank)
        fittest = rank[:10]
        dots = create(fittest)
        pos = 0
    disp.update()
pygame.quit()
