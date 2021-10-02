import time
from copy import deepcopy
st = time.time()

inputfile = "input11.txt"

def readinput():
    L = []
    with open(inputfile) as fp:
        for line in fp:
            line = line.strip()

            L.append(line)
            
    return L

def splitinput():
    L = [i.split("\n") for i in open(inputfile).read().split("\n\n")]

    return L

## Parse input
inp = readinput()
#inp = splitinput()

## Solve problem
sernum = int(inp[0])
cells = {}

for y in range(1, 301):
    cells[y] = {}
    for x in range(1, 301):
        rid = x + 10
        pl = (((rid * y + sernum) * rid) // 100) % 10 - 5
        cells[y][x] = pl

#print(cells[5][3])
cell = (0,0)
maxtpower = -5
def sumsqu(y,x,w):
    s = 0
    for ys in range(y, y+w):
        for xs in range(x, x+w):
            s += cells[ys][xs]
    return s

def growsqu(y,x,w,s):
    for xs in range(x, x+w):
        s += cells[y+w-1][xs]
    for ys in range(y, y+w-1):
        s+= cells[ys][x+w-1]
    return s

for ys in range(1, 299):
    for xs in range(1, 299):
        squ = sumsqu(ys, xs, 3)
        if squ > maxtpower:
            maxtpower = squ
            cell = (xs, ys)

print("Serial number:> ", sernum)
print("Largest total power 3x3 at:> ", cell)       

maxRsum = -99999999
maxRcelld = (0, 0, 0)
squares  = []

for w in range(2, 301):
    nextsquares = []
    if len(squares) == 0:
        for y in range(1, 302-w):
            for x in range(1, 302-w):
                squ = sumsqu(y, x, w)
                if squ > maxRsum:
                    maxRsum = squ
                    maxRcelld = (x, y, w)
                squares.append((y,x,squ))
    else:
        for sq in squares:
            y, x, s = sq[0], sq[1], sq[2]
            if y+w in cells and x+w in cells[y]:
                squ = growsqu(y, x, w, s)
                if squ > maxRsum:
                    maxRsum = squ
                    maxRcelld = (x, y, w)
                nextsquares.append((y,x,squ)) 
        squares = deepcopy(nextsquares)

print("Largest total power is:> ", maxRsum, "@", maxRcelld)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)