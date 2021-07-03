import time
from copy import deepcopy
import operator
st = time.time()

inputfile = "input6.txt"

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
scoords = dict()
gr = {}
gs = {}
infa = set()
cnrs = [[9999,9999] , [0,0]]
n = 1
tg = {}
target = 10000

class coord:
    def __init__(self, n=None, cs=0):
        self.nearest = n
        self.csum = cs

def calcsum(y,x):
    cs = 0
    for sco in scoords:
        cs += abs(y-scoords[sco][0]) + abs(x-scoords[sco][1])
    return cs

for p in inp:
    c = p.split(", ")
    c[0], c[1] = int(c[0]), int(c[1])

    if c[0] < cnrs[0][0]:
        cnrs[0][0] = c[0]-1
    if c[1] < cnrs[0][1]:
        cnrs[0][1] = c[1]-1
    if c[0] > cnrs[1][0]:
        cnrs[1][0] = c[0]+1
    if c[1] > cnrs[1][1]:
        cnrs[1][1] = c[1]+1
    
    scoords[n] = ((c[1], c[0]))
    gs[n] = 1
    n += 1

for sc in scoords:
    if not scoords[sc][1] in gr:
        gr[scoords[sc][1]] = {}
    if not scoords[sc][0] in gr[scoords[sc][1]]:
        gr[scoords[sc][1]][scoords[sc][0]] = coord(sc, calcsum(scoords[sc][1], scoords[sc][0]))

#print(gr)
#print(cnrs)

def printgr():
    for y in range(cnrs[0][0], cnrs[1][1]+1):
        line = ""
        for x in range(cnrs[0][1], cnrs[1][0]+1):
            if not y in gr or not x in gr[y]:
                line += " "
            else:
                line += str(gr[y][x].nearest)
        print(line)
    
def writegr():
    f = open("d6out.txt", "w")
    for y in range(cnrs[0][0], cnrs[1][1]+1):
        line = ""
        for x in range(cnrs[0][1], cnrs[1][0]+1):
            if not y in gr or not x in gr[y]:
                line += " "
            else:
                line += str(gr[y][x].nearest)
        f.write(line + "\n")
    f.close()

def fillround(poslist, mag):
    es = [ [0,1], [0,-1], [1,0], [-1,0] ]
    ngr = {}

    for pos in poslist:
        ip = gr[pos[0]][pos[1]].nearest
        for e in es:
            y, x = pos[0]+e[0], pos[1]+e[1]

            if x < cnrs[0][0] or x > cnrs[1][0] or y < cnrs[0][1] or y > cnrs[1][1]:
                # its gone to infinity
                #print("infinite")
                if not ip == ".":
                    infa.add(ip)
                continue

            # first check if the position in the grid is already set
            # if it is, it's already closer to another point
            if y in gr:
                if x in gr[y]:
                    continue
            # if it is not in the grid, add it to the list of grid updates
            if not y in ngr:
                ngr[y] = {}
            if not x in ngr[y]:
                ngr[y][x] = coord(ip, calcsum(y,x))
            else:
                if ngr[y][x].nearest == ip:
                    continue
                else:
                    ngr[y][x].nearest = (".")
                    #print("contested square")
    
    return ngr

#printgr()

fillfrom = []
for ys in gr:
    for xs in gr[ys]:
        fillfrom.append((ys, xs))

end = False
e = 1
while not end:
    ugr = fillround(fillfrom, e)
    #print(len(ugr))
    if len(ugr) == 0:
        end = True
        break
    fillfrom.clear()
    for ys in ugr:
        for xs in ugr[ys]:
            ip = ugr[ys][xs].nearest
            cs = ugr[ys][xs].csum
            fillfrom.append((ys, xs))
            if not ys in gr:
                gr[ys] = {}
            if not xs in gr[ys]:
                gr[ys][xs] = coord(ip, cs)
                if ip in gs:
                    gs[ip] += 1

    e += 1
    #printgr()
    #input()
#printgr()
#writegr()

for x in infa:
    gs.pop(x)
#print(gs)

print("Largest area:> ", max(gs.items(), key=operator.itemgetter(1))[1])

tsum = 0
for ys in gr:
    for xs in gr[ys]:
        if gr[ys][xs].csum < target:
            
            tsum += 1

print("Target region size:> ", tsum)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)