import time
from collections import defaultdict
st = time.time()

inputfile = "input23.txt"

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
nanobotp = dict()
nanobotr = dict()
bid = 0

## Solve problem
mmx = [999999,-999999]
mmy = [999999,-999999]
mmz = [999999,-999999]

for x in inp:
    coor = x.split(", ")
    pos = coor[0][5:-1].split(",")
    rad = int(coor[1][2:])
    nanobotr[bid] = rad
    nanobotp[bid] = (int(pos[0]), int(pos[1]), int(pos[2]))
    if nanobotp[bid][0] < mmx[0]:
        mmx[0] = nanobotp[bid][0]
    if nanobotp[bid][0] > mmx[1]:
        mmx[1] = nanobotp[bid][0]
    if nanobotp[bid][1] < mmy[0]:
        mmy[0] = nanobotp[bid][1]
    if nanobotp[bid][1] > mmy[1]:
        mmy[1] = nanobotp[bid][1]
    if nanobotp[bid][2] < mmz[0]:
        mmz[0] = nanobotp[bid][2]
    if nanobotp[bid][2] > mmz[1]:
        mmz[1] = nanobotp[bid][2]
    bid += 1

maxrad = max(nanobotr, key=lambda x:nanobotr[x])

inrange = 0
out_of_range = dict()
maxdist = 0

#print(mmx, mmy, mmz)

for y in nanobotp:
    dist = abs(nanobotp[maxrad][0] - nanobotp[y][0]) +\
        abs(nanobotp[maxrad][1] - nanobotp[y][1]) +\
        abs(nanobotp[maxrad][2] - nanobotp[y][2])
    
    if dist <= nanobotr[maxrad]:
        if dist > maxdist:
            maxdist = dist
        inrange += 1

print("No. bots in range of strongest:> ", inrange)

mulp = [1,3,5,7,9]
xw = abs(mmx[0]) + abs(mmx[1])
yw = abs(mmy[0]) + abs(mmy[1])
zw = abs(mmz[0]) + abs(mmz[1])
maxs = defaultdict(list)

final = False
while not final:
    if xw < 10 or yw < 10 or zw < 10:
        xw, yw, zw = 10, 10, 10
        final = True
    maxinrange = 0
    # x,y,z
    mirpos = (0,0,0)
   
    xp = xw // 10
    yp = yw // 10
    zp = zw // 10

    for zs in mulp:
        for ys in mulp:
            for xs in mulp:
                inrangeme = 0
                p = [mmx[1]-(xp*xs), mmy[1]-(yp*ys), mmz[1]-(zp*zs)]

                for z in nanobotp:
                    dist = abs(p[0] - nanobotp[z][0]) +\
                        abs(p[1] - nanobotp[z][1]) +\
                        abs(p[2] - nanobotp[z][2])
                    
                    if dist <= nanobotr[z]:
                        inrangeme += 1
                
                if inrangeme > maxinrange:
                    maxinrange = inrangeme
                    mirpos = (p[0], p[1], p[2])
    
    #print(maxinrange, mirpos)
    #print(xw,yw,zw)
    #input()
    maxs[maxinrange].append(mirpos)
    xw *= 0.9
    yw *= 0.9
    zw *= 0.9
    mmx = [mirpos[0]-(xw//2), mirpos[0]+(xw//2)]
    mmy = [mirpos[1]-(yw//2), mirpos[1]+(yw//2)]
    mmz = [mirpos[2]-(zw//2), mirpos[2]+(zw//2)]

mmmm = max(maxs.keys())
msum = 9999999999999
for s in maxs[mmmm]:
    if sum(s) < msum:
        msum = sum(s)
print("Distance from closest point:> ", int(msum))
#for zs in out_of_range:
#    print(out_of_range[zs])

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)