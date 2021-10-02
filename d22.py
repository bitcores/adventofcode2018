import time
from collections import defaultdict
from copy import deepcopy
st = time.time()

inputfile = "input22.txt"

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
d = inp[0].split(": ")
t = inp[1].split(": ")
depth = int(d[1])
target = t[1].split(",")
#swap x,y yto y,x
target[0], target[1] = int(target[1]), int(target[0])
ent = (0,0)
#print("Target is at x:", target[1], "y:", target[0])

# store (geoindex, eroindex, type) as tuple
geo = defaultdict(dict)
scoremap = dict()
scoremap[0] = defaultdict(dict)
scoremap[1] = defaultdict(dict)
scoremap[2] = defaultdict(dict)
scoremap[1][0][0] = 0

def DrawMap(has=None):
    for y in geo:
        line = ""
        for x in geo[y]:
            e = geo[y][x]
            if not has == None and (y,x) in has:
                line += "#"
            elif y == target[0] and x == target[1]:
                line += "T"
            elif e[2] == 0:
                line += "."
            elif e[2] == 1:
                line += "="
            elif e[2] == 2:
                line += "|"
        print(line)


# modify this so that it will expand the size of the grid by +1,+1
# do x+1 first for existing ys, then do y+1
def GrowGeo():
    mx = max(geo[0].keys())
    my = max(geo.keys())
    for y in range(0, my+1):
        CalcGeo(y, mx+1)
    
    for x in range(0, mx+2):
        CalcGeo(my+1, x)


def CalcGeo(y,x):
    if y == 0:
        gi = x * 16807
    elif x == 0:
        gi = y * 48271
    else:
        gi = geo[y-1][x][1] * geo[y][x-1][1]

    ei = (gi + depth) % 20183
    typ = ei % 3
    geo[y][x] = (gi, ei, typ)


def GetDists(p):
    drs = [ [1,0], [-1,0], [0,1], [0,-1] ]
    exp = defaultdict(set)
    exp[0].add(p)
    ttl = 999999
    up = set()
    step = 0
    while True:

        if step > ttl:
            break

        moves = 0
        for e in range(0, 8):
            exp[e] = exp[e].union(exp[e+1])
            exp[e+1].clear()
            moves += len(exp[e])
        if moves == 0:
            # exit
            break

        nexp = defaultdict(set)

        for e in exp[0]:
            if e[0] == target[0] and e[1] == target[1]:
                s = step
                if not e[2] == 1:
                    s += 7
                if not e[1] in scoremap[1][e[0]] or scoremap[1][e[0]][e[1]] > s:
                    scoremap[1][e[0]][e[1]] = s
                ttl = s
                
                #print("Target reached at @", s)
                continue
            else:
                if not e[1] in scoremap[e[2]][e[0]] or scoremap[e[2]][e[0]][e[1]] > step:
                    scoremap[e[2]][e[0]][e[1]] = step

            for d in drs:
                y, x, t = e[0]+d[0], e[1]+d[1], e[2]

                if x < 0 or y < 0:
                    continue
                
                if not y in geo:
                    GrowGeo()
                elif not x in geo[y]:
                    GrowGeo()
                
                if x in scoremap[t][y] and scoremap[t][y][x] <= step:
                    continue

                # check for moving between tool regions etc
                if geo[y][x][2] == 0:
                    if t == 0:
                        if geo[e[0]][e[1]][2] == 1:
                            nexp[8].add((y,x,2))
                        elif geo[e[0]][e[1]][2] == 2:
                            nexp[8].add((y,x,1))
                        else:
                            print("This should never occur rock")
                            continue
                    else:
                        nexp[0].add((y,x,t))
                        up.add((y,x))
                elif geo[y][x][2] == 1:
                    if t == 1:
                        if geo[e[0]][e[1]][2] == 0:
                            nexp[8].add((y,x,2))
                        elif geo[e[0]][e[1]][2] == 2:
                            nexp[8].add((y,x,0))
                        else:
                            print("This should never occur wet")
                            continue
                    else:
                        nexp[0].add((y,x,t))
                        up.add((y,x))
                elif geo[y][x][2] == 2:
                    if t == 2:
                        if geo[e[0]][e[1]][2] == 0:
                            nexp[8].add((y,x,1))
                        elif geo[e[0]][e[1]][2] == 1:
                            nexp[8].add((y,x,0))
                        else:
                            print("This should never occur narrow")
                            continue
                    else:
                        nexp[0].add((y,x,t))
                        up.add((y,x))

        step += 1
        
        #DrawMap(up)
        #input()
        up.clear()
        exp[0].clear()
        exp[0] = deepcopy(nexp[0])
        exp[8] = deepcopy(nexp[8])
    return()

for ys in range(ent[0], target[0]+1):
    for xs in range(ent[1], target[1]+1):
        gi = 0
        if ys == 0 and xs == 0:
            gi = 0
        elif ys == target[0] and xs == target[1]:
            gi = 0
        elif ys == 0:
            gi = xs * 16807
        elif xs == 0:
            gi = ys * 48271
        else:
            gi = geo[ys-1][xs][1] * geo[ys][xs-1][1]

        ei = (gi + depth) % 20183
        typ = ei % 3
        geo[ys][xs] = (gi, ei, typ)

risk = 0
for y in geo:
    for x in geo[y]:
        if y <= target[0] and x <= target[1]:
            risk += geo[y][x][2]

print("Risk level:> ", risk)


# y, x, tool
pos = (0,0,1)
timetotarget = GetDists(pos)

print("Shortest time to target:> ", scoremap[1][target[0]][target[1]])

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)