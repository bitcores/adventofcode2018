import time
from copy import deepcopy
from collections import defaultdict
import re
st = time.time()

inputfile = "input20.txt"

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
#[y, x]
ptr = 0
pos = [0, 0]
fmap = defaultdict(dict)
doordist = defaultdict(dict)
fmap[pos[0]][pos[1]] = "X"
move = { "N": (-1,0), "S": (1,0), "W": (0,-1), "E": (0,1) }  
parpar = {}
mmy = [99999, -99999]
mmx = [99999, -99999]

def PrintMap():
    for y in range(mmy[0], mmy[1]+1):
        line = ""
        c = mmx[0]
        for x in range(mmx[0],mmx[1]+1):
            if x in fmap[y]:
                for _ in range(c, x):
                    line += " "
                if x in doordist[y]:
                    line += str(doordist[y][x])
                else:
                    line += fmap[y][x]
                c = x +1
        print(line)

def WriteMap():
    f = open("d20map.txt", "w")
    for y in range(mmy[0], mmy[1]+1):
        line = ""
        c = mmx[0]
        for x in range(mmx[0],mmx[1]+1):
            if x in fmap[y]:
                for _ in range(c, x):
                    line += " "
                line += fmap[y][x]
                c = x +1
        f.write(line + "\n")
    f.close()

def mover(dm, bras, cptr):
    #print(dm, bras, cptr)
    sp = {}
    newbras = {}
    bradepth = 0
    while cptr < len(dm) and not dm[cptr] == "$":
        #print(dm, bras, cptr)

        if dm[cptr] == "^":
            cptr += 1
            continue

        elif dm[cptr] == "(":
            bradepth += 1
            newbras[bradepth] = set()
            sp[bradepth] = deepcopy(bras)
            
        elif dm[cptr] == "|":
            newbras[bradepth] = newbras[bradepth].union(deepcopy(bras))
            bras = deepcopy(sp[bradepth])
        
        elif dm[cptr] == ")":
            newbras[bradepth] = newbras[bradepth].union(deepcopy(bras))
            bras = deepcopy(newbras[bradepth])
            bradepth -= 1

        elif dm[cptr] in move:
            tbras = set()
            for cpos in bras:
                m = move[dm[cptr]]
                cpos = (cpos[0]+m[0], cpos[1]+m[1])
                if not cpos[1] in fmap[cpos[0]]:
                    #if dm[cptr] == "W" or dm[cptr] == "E":
                    #    fmap[cpos[0]][cpos[1]] = "|"
                    #else:
                    #    fmap[cpos[0]][cpos[1]] = "-"
                    fmap[cpos[0]][cpos[1]] = "|"
                cpos = (cpos[0]+m[0], cpos[1]+m[1])
                if not cpos[1] in fmap[cpos[0]]:
                    fmap[cpos[0]][cpos[1]] = "."
                if cpos[0] < mmy[0]:
                    mmy[0] = cpos[0]
                if cpos[0] > mmy[1]:
                    mmy[1] = cpos[0]
                if cpos[1] < mmx[0]:
                    mmx[0] = cpos[1]
                if cpos[1] > mmx[1]:
                    mmx[1] = cpos[1]
                tbras.add(cpos)
            bras = deepcopy(tbras)

        cptr += 1
    return

def DoorCounter(mvrs):
    cuntr = 0
    rooms = 0
    ds = [ [0,1], [1,0], [0,-1], [-1,0] ]
    
    
    while len(mvrs) > 0:
        cuntr += 1
        nmvrs = []
        for m in mvrs:
            for d in ds:
                c = deepcopy(m)
                c[0], c[1] = m[0]+d[0], m[1]+d[1]
                if c[1] in fmap[c[0]]:
                    if fmap[c[0]][c[1]] == "|":
                        if not c[1] in doordist[c[0]]:
                            doordist[c[0]][c[1]] = cuntr
                            nmvrs.append([c[0]+d[0],c[1]+d[1]])
                            if cuntr >= 1000:
                                rooms += 1
        mvrs.clear()
        mvrs = deepcopy(nmvrs)
    
    return(cuntr-1, rooms)

for d in inp:
    fmap = defaultdict(dict)
    doordist = defaultdict(dict)
    fmap[pos[0]][pos[1]] = "X"
    b = set()
    b.add((0,0))
    mover(d, b, 0)

    #PrintMap()
    #WriteMap()

    # map is ready
    # now we have to find the room that required passing through the most
    # number of doors to reach.
    maxdist, rooms = DoorCounter([[0,0]])
    #PrintMap()
    print("Furtherest room:> ", maxdist)
    print("Rooms more than 1000 doors away:> ", rooms)
    #input() 

        
## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)