import pgerom as pe
from random import randint
pe.init()
pe.display.make((700,600),"Snake")

# FACTORS
tailsize = 3
headsize = 5
shadowsize = 4
shadowcolor = (240, 240, 240)
shadowcolor2 = (230, 230, 230)
yumsize = 1

class snake:
    def __init__(self, position, color = (0, 255, 0), size=5):
        self.pos = position
        self.size = size
        self.pie = []
        self.yum = []
        self.color = color
        self.rot = 0
        for i in range(self.size):
            self.pie.append(self.pos)
            self.yum.append(False)
    def draw(self):
        color = self.color
        c = 1
        c2 = tailsize
        c3 = tailsize
        m = 0.5/self.size
        m2 = (headsize-tailsize)/self.size
        c3 += m2
        pe.draw.circle(shadowcolor, self.pos, headsize, 0)
        pe.draw.circle(color, self.pos, headsize, 0)
        linep = self.pos
        for i in self.pie:
            pe.draw.circle(shadowcolor, i, c2+shadowsize, 0)
            pe.draw.line(shadowcolor2, linep, i, int(c3*2)+shadowsize*2)
            linep = i
        for i in self.yum:
            color = (self.color[0] * c, self.color[1] * c, self.color[2] * c)
            c -= m
            if i:
                pe.draw.circle(color, i, yumsize, 0)
        color = self.color
        c = 0.5
        self.pie.reverse()
        linep = self.pie[0]
        for i in self.pie:
            color = (self.color[0]*c, self.color[1]*c, self.color[2]*c)
            color2 = (max(0, color[0]-10), max(0, color[1]-10), max(0, color[2]-10))
            c += m
            c2 += m2
            c3 += m2
            pe.draw.circle(color, i, c2, 0)
            pe.draw.line(color2, linep, i, int(c3*2))
            linep = i
        self.pie.reverse()
    def shift(self):
        # PIE
        if pe.math.dist(self.pie[0], self.pos) >= 1:
            self.pie.insert(0, self.pos)
            del self.pie[len(self.pie)-1]
        # YUM
        self.yum.insert(0, False)
        del self.yum[len(self.yum)-1]
    def move(self, toward, clearance):
        if pe.math.dist(self.pos, toward) < 2:
            self.pos = toward
        if pe.math.dist(self.pos, toward) < 11:
            self.pos = pe.math.lerp(self.pos, toward, 1)
        else:
            self.pos = pe.math.lerp(self.pos, toward, 5)
        self.shift()
    def expand(self, net=1):
        for i in range(net):
            self.size += 1
            self.pie.append(self.pos)
        self.yum.insert(0,self.pos)
        if net < 2:
            return
        for i in range(net-1):
            self.yum.insert(0, self.pos)
class apple:
    def __init__(self, position, color = (200, 50, 50), net = 2):
        self.pos = position
        self.net = net
        self.color = color
    def check(self, head):
        return pe.math.dist(self.pos, head) <= 10
    def draw(self):
        pe.draw.circle(self.color, self.pos, 8, 0)
def apple_generator(head):
    random_pos = (randint(25, 675),randint(25, 575))
    while pe.math.dist(random_pos, head) < 100:
        random_pos = (randint(25, 675),randint(25, 575))
    return random_pos
def head_calculate(snk, toward):
    tsx = pe.math.tsx.make(snk.pos, 15)
    best = 2
    bestnum = 0
    current=0
    for p in tsx:
        closenest = min(pe.math.dist(p, pe.math.lerp(snk.pos, toward, 15))/15,1)
        if closenest < best:
            best = closenest
            bestnum = current
        current += 1
    #pe.draw.circle(pe.color.blue, tsx[bestnum], 3, 0) # Rotation testing dot
    rotmin = bestnum
    rot = rotmin
    #pe.draw.circle(pe.color.black, pe.math.tsx.get(tsx,rot/10), 3, 0) # Rotation testing dot
    return tsx, rot, bestnum
def head_calculate_2(snk, toward, tsx, bestnum):
    rot = bestnum/10
    snk_rot = snk.rot/10
    rot = min(max(snk_rot+90, rot),snk_rot-90)
    rot *= 10
    rot = snk.rot+10
    return rot
# Variables
snake1 = snake(pe.math.center((0, 0, 700, 600)), size=10)
speed = 50
apple1 = apple(apple_generator(snake1.pos),net=1)
lastms = (0,0)
opss = 0

while True:
    for pe.event.c in pe.event.get():
        pe.event.quitcheckauto()
    pe.fill.full(pe.color.white)

    snake1.draw()
    apple1.draw()
    ms = pe.mouse.pos()
    #ms = apple1.pos
    if opss >= 5:# or True:
        lastms=ms
        opss = 0

    tsx, rot, bestnum = head_calculate(snake1, ms)
    pos = pe.math.tsx.get(tsx, (snake1.rot - 900 / 10) + 180)
    move = True
    if ms == lastms and pe.math.dist(ms, snake1.pos)>50:
        snake1.rot = rot
        if apple1.check(snake1.pos):
            apple1.pos = apple_generator(snake1.pos)
            snake1.expand()
    elif ms == lastms:
        if apple1.check(ms):
            pos = ms
        else:
            pos = ms
    else:
        pass
        tsx, rot, bestnum = head_calculate(snake1, lastms)
        snake1.rot = rot
        pos = pe.math.tsx.get(tsx, (snake1.rot - 900 / 10) + 180)
    if move:
        snake1.move(pos, speed)

    if apple1.check(snake1.pos):
        apple1.pos = apple_generator(snake1.pos)
        snake1.expand(apple1.net)

    pe.time.tick(60000)
    if ms != lastms:
        opss += 1
    pe.display.update()
