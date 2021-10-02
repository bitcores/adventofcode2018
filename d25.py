import time
from collections import defaultdict
st = time.time()

inputfile = "input25.txt"

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
stars = dict()
sid = 0
constellations = defaultdict(set)
cid = 0

for i in inp:
    co = i.split(",")
    stars[sid] = (int(co[0]), int(co[1]), int(co[2]), int(co[3]))
    sid += 1

for s in stars:
    mcon = []
    for c in constellations:
        for e in constellations[c]:
            mhat = 0
            for x in range(len(stars[s])):
                mhat += abs(stars[s][x] - stars[e][x])
            if mhat <= 3 and not c in mcon:
                mcon.append(c)

    if len(mcon) == 0:
        constellations[cid].add(s)
        cid += 1
    elif len(mcon) == 1:
        constellations[mcon[0]].add(s)
    elif len(mcon) > 1:
        for y in range(1, len(mcon)):
            constellations[mcon[0]] = constellations[mcon[0]].union(constellations[mcon[y]])
            constellations.pop(mcon[y])
        constellations[mcon[0]].add(s)
    
    #print(constellations)
    #input()

print("No. of constellations:> ", len(constellations))

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)