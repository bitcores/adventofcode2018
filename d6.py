import time
import operator
from PIL import Image, ImageDraw
from math import floor
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
# all coords will be in (y, x) format
scoords = dict()
gr = {}
gs = {}
infa = set()
cnrs = [[9999,9999] , [0,0]]
n = 1
tg = {}
target = 10000
targreg = []
colors = {".": (0,0,0)}

def calcsum(y,x):
    cs = 0
    for sco in scoords:
        cs += abs(y-scoords[sco][0]) + abs(x-scoords[sco][1])
    return cs

for p in inp:
    c = p.split(", ")
    x, y = int(c[0]), int(c[1])

    if y < cnrs[0][0]:
        cnrs[0][0] = y-1
    if x < cnrs[0][1]:
        cnrs[0][1] = x-1
    if y > cnrs[1][0]:
        cnrs[1][0] = y+1
    if x > cnrs[1][1]:
        cnrs[1][1] = x+1
    
    scoords[n] = (y, x)
    gs[n] = 1
    n += 1

for sc in scoords:
    if not scoords[sc][0] in gr:
        gr[scoords[sc][0]] = {}
    if not scoords[sc][1] in gr[scoords[sc][0]]:
        gr[scoords[sc][0]][scoords[sc][1]] = sc
        if calcsum(scoords[sc][0], scoords[sc][1]) < target:
            targreg.append((scoords[sc][0], scoords[sc][1]))

colordiv = floor((255 / (len(gs) / 3)) / 1.5)
r, g, b = 255, 0, 0
for c in gs.keys(): 
    colors[c] = (r, g, b)
    if r > 0:
        r -= colordiv
        if r < 0:
            r = 0
        g += colordiv
        if g > 255:
            g = 255
    else:
        g -= colordiv
        if g < 0:
            g = 0
        b += colordiv
        if b > 255:
            b = 255

#print(colors)


#print(gr)
#print(cnrs)

def printgr():
    for x in range(cnrs[0][0], cnrs[1][0]+1):
        line = ""
        for y in range(cnrs[0][1], cnrs[1][1]+1):
            if not y in gr or not x in gr[y]:
                line += " "
            else:
                line += str(gr[y][x])
        print(line)
    
def writegr():
    yo = cnrs[0][0]
    xo = cnrs[0][1]
    img = Image.new("RGB", (cnrs[1][0]-yo+1, cnrs[1][1]-xo+1), (255, 255, 255))
    for y in range(cnrs[0][0], cnrs[1][0]+1):
        for x in range(cnrs[0][1], cnrs[1][1]+1):
            if not y in gr or not x in gr[y]:
                img.putpixel((y-yo, x-xo), (255, 255, 255))
            else:
                img.putpixel((y-yo, x-xo), colors[gr[y][x]])

    for ta in targreg:
        inv = colors[gr[ta[0]][ta[1]]]
        inv = (255-inv[0],255-inv[1],255-inv[2])
        img.putpixel((ta[0]-yo, ta[1]-xo), inv)

    img.save("d6out.png")

def fillround(poslist, mag):
    es = [ [0,1], [0,-1], [1,0], [-1,0] ]
    ngr = {}

    for pos in poslist:
        ip = gr[pos[0]][pos[1]]
        for e in es:
            y, x = pos[0]+e[0], pos[1]+e[1]

            if y < cnrs[0][0] or y > cnrs[1][0] or x < cnrs[0][1] or x > cnrs[1][1]:
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
                ngr[y][x] = ip
                if calcsum(y,x) < target:
                    targreg.append((y, x))
            else:
                if ngr[y][x] == ip:
                    continue
                else:
                    ngr[y][x] = (".")
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
            ip = ugr[ys][xs]
            fillfrom.append((ys, xs))
            if not ys in gr:
                gr[ys] = {}
            if not xs in gr[ys]:
                gr[ys][xs] = ip
                if ip in gs:
                    gs[ip] += 1

    e += 1
    #printgr()
    #input()
#printgr()
writegr()

for x in infa:
    gs.pop(x)
#print(gs)

print("Largest area:> ", max(gs.items(), key=operator.itemgetter(1))[1])
print("Target region size:> ", len(targreg))

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)