import time
from copy import deepcopy
st = time.time()

inputfile = "input10.txt"

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
points = dict()
p = 0
for l in inp:
    x = l.find("n=<")
    y = l.find(">", x)
    pos = l[x+3:y].split(",")

    x = l.find("y=<")
    y = l.find(">", x)
    vel = l[x+3:y].split(",")
    #print(pos, vel)
    points[p] = dict()
    points[p]["pos"] = (int(pos[0].strip()), int(pos[1].strip()))
    points[p]["vel"] = (int(vel[0].strip()), int(vel[1].strip()))
    p += 1

#print(len(points))

def buildgrid():
    grid = dict()
    bounds = [9999,9999,-9999,-9999]
    for p in points:
        x, y = points[p]["pos"][0], points[p]["pos"][1]
        if x < bounds[1]:
            bounds[1] = x
        if x > bounds[3]:
            bounds[3] = x
        if y < bounds[0]:
            bounds[0] = y
        if y > bounds[2]:
            bounds[2] = y

        if not y in grid:
            grid[y] = dict()
        grid[y][x] = "#"
    
    return grid, bounds

def printgrid(grid, bounds):
    for y in range(bounds[0], bounds[2]+1):
        line = ""
        for x in range(bounds[1], bounds[3]+1):
            if y in grid:
                if x in grid[y]:
                    line += grid[y][x]
                else:
                    line += "."
            else:
                line += "."
        print(line)

grid, bounds = buildgrid()
timer = 0
while(True):
    for p in points:
        points[p]["pos"] = (points[p]["pos"][0]+points[p]["vel"][0], points[p]["pos"][1]+points[p]["vel"][1])
    oldbounds = deepcopy(bounds)
    oldgrid = deepcopy(grid)
    ow, oh = oldbounds[3]-oldbounds[1], oldbounds[2]-oldbounds[0]
    grid, bounds = buildgrid()
    w, h = bounds[3]-bounds[1], bounds[2]-bounds[0]
    if ow*oh < w*h:
        break
    timer += 1

print("Printing Navigation Message:>")
printgrid(oldgrid, oldbounds)
print("Message appeared in:> ", timer, "seconds")

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)