import time
from collections import defaultdict
st = time.time()

inputfile = "input12.txt"

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
init = inp[0][15:]
rules = {}
pots = defaultdict(lambda: ".")

def pots2str():
    line = ""
    for p in range(min(pots.keys()), max(pots.keys())):
        line += pots[p]
    return line

def subpots(p):
    sp = ""
    for e in range(p-2, p+3):
        sp += pots[e]
    return sp

for i in range(2,len(inp)):
    r = inp[i].split(" => ")
    rules[r[0]] = r[1]

for p in range(0,len(init)):
    pots[p] = init[p]

#print(rules)

mem = {}
mem[0] = pots2str()

for i in range(1, 50_000_000_001):
    updates = {}
    s,e = min(pots.keys())-2, max(pots.keys())+3

    for pot in range(s, e):
        subpot = subpots(pot)
        #print(subpot)
        if subpot in rules:
            #print(subpot, rules[subpot])
            updates[pot] = rules[subpot]
        else:
            updates[pot] = "."
    
    for u in updates:
        pots[u] = updates[u]
    updates.clear()

    removes = []
    for x in range(min(pots.keys()), max(pots.keys())):
        if pots[x] == "#":
            break
        else:
            removes.append(x)
    for y in range(max(pots.keys()), min(pots.keys()), -1):
        if pots[y] == "#":
            break
        else:
            removes.append(y)
    
    for r in removes:
        pots.pop(r)

    if pots2str() in mem.values():
        loopoffset = i
        break

    mem[i] = pots2str()
    #print(pots2str())

    if i == 20:
        potsum = 0
        for x in pots:
            if pots[x] == "#":
                potsum += x
        print("Sum of potted plant numbers @ 20th gen:> ", potsum)

shift = 50_000_000_000 - loopoffset   

potsum = 0
for x in pots:
    if pots[x] == "#":
        potsum += (x + shift)
print("Sum of potted plant numbers @ 50,000,000,000th gen:> ", potsum)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)