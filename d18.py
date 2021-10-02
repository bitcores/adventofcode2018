import time
from collections import defaultdict
st = time.time()

inputfile = "input18.txt"

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
def PrintArea():
    for y in area:
        line = ""
        for x in area[y]:
            line += area[y][x]
        print(line)

def CountAround(y, x):
    o, l, t = 0, 0, 0
    for c in circ:
        ys, xs = y+c[0], x+c[1]
        if not ys in area:
            continue
        if not xs in area[ys]:
            continue
        if area[ys][xs] == ".":
            o += 1
        if area[ys][xs] == "#":
            l += 1
        if area[ys][xs] == "|":
            t += 1
    return((o, l, t))

def EncodeArea():
    encoded = []
    for ys in area:
        enc = 0
        for xs in area[ys]:
            enc *= 3
            if area[ys][xs] == ".":
                enc += 0
            if area[ys][xs] == "|":
                enc += 1
            if area[ys][xs] == "#":
                enc += 2
        encoded.append(enc)
    return encoded

def DecodeArea(enc):
    sx = len(area[0])
    for y in range(len(enc)):
        g = enc[y]
        vals = []
        for _ in range(sx):
            v = g % 3
            vals.insert(0, v)
            g = g // 3
        
        for x in range(len(vals)):
            if vals[x] == 0:
                area[y][x] = "."
            if vals[x] == 1:
                area[y][x] = "|"
            if vals[x] == 2:
                area[y][x] = "#"



circ = [(-1, -1), (-1, 0), (-1, 1),\
    (0, -1), (0, 1), \
    (1, -1), (1, 0), (1, 1)]

area = {}

for l in range(len(inp)):
    if not l in area:
        area[l] = {}
    for i in range(len(inp[l])):
        area[l][i] = inp[l][i]

#PrintArea()

mem = []
loops = 0
loope = 0
for i in range(1, 1_000_000_000):
    changes = defaultdict(dict)

    for y in area:
        for x in area[y]:
            e = area[y][x]
            surr = CountAround(y, x)
            if e == "." and surr[2] >= 3:
                changes[y][x] = "|"
            if e == "|" and surr[1] >= 3:
                changes[y][x] = "#"
            if e == "#" and (surr[1] < 1 or surr[2] < 1):
                changes[y][x] = "."
    
    for yn in changes:
        for xn in changes[yn]:
            area[yn][xn] = changes[yn][xn]

    #PrintArea()
    #input()

    lum, tre = 0, 0
    for ys in area:
        lum += list(area[ys].values()).count("#")
        tre += list(area[ys].values()).count("|")
    score = lum * tre

    if i == 10:
        print("Resource value after 10 mins:> ", score)
    
    encarea = EncodeArea()
    if encarea in mem:
        loope = i-1
        loops = mem.index(encarea)
        #print("Loop found @ ", i, "from ", loops)
        break
    mem.append(encarea)

red = 1_000_000_000 - loops
offset = red % (loope - loops)
encd = mem[(loops-1)+offset]

DecodeArea(encd)
lum, tre = 0, 0
for ys in area:
    lum += list(area[ys].values()).count("#")
    tre += list(area[ys].values()).count("|")
score = lum * tre
print("Resource value after 1 billion mins:> ", score)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)