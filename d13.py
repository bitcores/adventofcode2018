import time
from copy import deepcopy
st = time.time()

inputfile = "input13.txt"

def readinput():
    L = []
    with open(inputfile) as fp:
        for line in fp:
            line = line.rstrip()

            L.append(line)
            
    return L

def splitinput():
    L = [i.split("\n") for i in open(inputfile).read().split("\n\n")]

    return L

## Parse input
inp = readinput()
#inp = splitinput()

## Solve problem
#coords are (y,x)
class cart:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        self.turn = 0
        self.crashed = False

carts = {}
dirs = { '<': (0,-1), '>': (0,1), 'v': (1,0), '^': (-1,0) }
carttypes = ['<', '^', '>', 'v']
trackgrid = {}

cid = 0
y = 0
for l in inp:
    x = 0
    trackgrid[y] = {}
    for c in l:
        if not c == " ":
            # check if c is a cart
            if c in carttypes:
                carts[cid] = cart(c, (y,x))
                cid += 1
                if c == "v" or c == "^":
                    trackgrid[y][x] = "|"
                else:
                    trackgrid[y][x] = "-"
            else:
                trackgrid[y][x] = c
        x += 1
    y += 1

def printtrack():
    for y in trackgrid:
        line = ""
        last = 0
        for x in trackgrid[y]:
            for _ in range(last, x):
                line += " "

            iscart = None
            for c in carts:
                if carts[c].pos == (y,x):
                    if not iscart == None:
                        iscart = "X"
                        break
                    else:
                        iscart = carts[c].type

            if not iscart == None:
                line += iscart
            else:
                line += trackgrid[y][x]
            last = x+1
        print(line)

def moveorder():
    order = []
    for c in carts:
        if carts[c].crashed:
            continue
        p = None
        for cid in order:
            if carts[c].pos[0] < carts[cid].pos[0] or \
                (carts[c].pos[0] == carts[cid].pos[0] and carts[c].pos[1] < carts[cid].pos[1]):
                p = order.index(cid)
                break
        if not p == None:
            order.insert(p, c)
        else:
            order.append(c)
    return deepcopy(order)

#printtrack()
#print([carts[x].pos for x in carts])

cartorder = moveorder()
turn = 0
run = True
first = False
#print(cartorder)

while run:
    turn += 1
    for c in cartorder:
        if carts[c].crashed:
            continue

        t = carts[c].type
        ti = carttypes.index(t)
        carts[c].pos = (carts[c].pos[0]+dirs[t][0], carts[c].pos[1]+dirs[t][1])
        y, x = carts[c].pos[0], carts[c].pos[1]
        # check if any other carts occupy this position, crash
        for cs in carts:
            if cs == c:
                continue
            if carts[cs].crashed:
                continue
            if carts[cs].pos == carts[c].pos:
                #print(c, "and", cs, "crashed")
                if not first:
                    print("First crash at:> ", str(carts[c].pos[1])+","+str(carts[c].pos[0]))
                    first = True
                carts[cs].crashed = True
                carts[c].crashed = True
                break
        
        if carts[c].crashed:
            continue

        # check for / and \, and turn the cart in the correct direction
        if trackgrid[y][x] == "/":
            if t == ">":
                carts[c].type = carttypes[1]
            elif t == "v":
                carts[c].type = carttypes[0]
            elif t == "<":
                carts[c].type = carttypes[3]
            elif t == "^":
                carts[c].type = carttypes[2]
        elif trackgrid[y][x] == "\\":
            if t == ">":
                carts[c].type = carttypes[3]
            elif t == "v":
                carts[c].type = carttypes[2]
            elif t == "<":
                carts[c].type = carttypes[1]
            elif t == "^":
                carts[c].type = carttypes[0]

        # check for + and turn the cart according to cart.turn (0, left, 1, straight, 2, right, 0)
        if trackgrid[y][x] == "+":
            if carts[c].turn == 0:
                ti -= 1
            if carts[c].turn == 2:
                ti += 1

            if ti < 0:
                ti = 3
            if ti > 3:
                ti = 0
            
            carts[c].type = carttypes[ti]

            carts[c].turn += 1
            if carts[c].turn > 2:
                carts[c].turn = 0

    #printtrack()
    #input()
    cartorder = moveorder()
    if len(cartorder) == 1:
        print("Location of last cart:> " , str(carts[cartorder[0]].pos[1])+","+str(carts[cartorder[0]].pos[0]))
        break

#printtrack()

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)