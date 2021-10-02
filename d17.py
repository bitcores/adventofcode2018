import time
from copy import deepcopy
st = time.time()

inputfile = "input17.txt"

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
mmx = [99999, -99999]
mmy = [99999, -99999]
reservoir = {}
reservoir[0] = {}
reservoir[0][500] = "+"

for l in inp:
    eb = l.split(", ")
    xs = []
    ys = []
    for p in eb:
        if p[0] == "x":
            xs = [int(a) for a in p[2:].split("..")]
        if p[0] == "y":
            ys = [int(a) for a in p[2:].split("..")]
        
    for y in range(ys[0], ys[-1]+1):
        if not y in reservoir:
            reservoir[y] = {}
        for x in range(xs[0], xs[-1]+1):
            reservoir[y][x] = "#"
    
    if xs[0] < mmx[0]:
        mmx[0] = xs[0]
    if xs[-1] > mmx[1]:
        mmx[1] = xs[-1]
    if ys[0] < mmy[0]:
        mmy[0] = ys[0]
    if ys[-1] > mmy[1]:
        mmy[1] = ys[-1]

def PrintGround():
    f = open("d17out.txt", "w")
    for ys in range(0, mmy[1]+1):
        line = ""
        for xs in range(mmx[0], mmx[1]+1):
            if not ys in reservoir:
                line += "."
            elif xs in reservoir[ys]:
                line += reservoir[ys][xs]
            else:
                line += "."
        #print(line)
        f.write(line + "\n")
    f.close()
        

#print(mmy, mmx)
#PrintGround()

overflow = False
wfs = {0: [0, 500]}
wfid = 1
while not overflow:
    clrwf = []
    addwf = {}
    #print(wfs)
    for wf in wfs:
        if wfs[wf][0]+1 in reservoir:
            if wfs[wf][1] in reservoir[wfs[wf][0]+1]:
                if reservoir[wfs[wf][0]+1][wfs[wf][1]] == "#" or reservoir[wfs[wf][0]+1][wfs[wf][1]] == "~":
                    fill = [True, True]
                    left = None
                    for x in range (wfs[wf][1]-1, mmx[0]-2, -1):
                        # look below
                        if x in reservoir[wfs[wf][0]+1]:
                            if not reservoir[wfs[wf][0]+1][x] == "#" and not reservoir[wfs[wf][0]+1][x] == "~":
                                left = x
                                fill[0] = False
                                break
                        else:
                            left = x
                            fill[0] = False
                            break
                        # look in current space
                        if x in reservoir[wfs[wf][0]]:
                            if reservoir[wfs[wf][0]][x] == "#":
                                left = x+1
                                break
                    if left == None:
                        left = mmx[0]-1

                    right = None
                    for x in range (wfs[wf][1]+1, mmx[1]+1):
                        # look below
                        if x in reservoir[wfs[wf][0]+1]:
                            if not reservoir[wfs[wf][0]+1][x] == "#" and not reservoir[wfs[wf][0]+1][x] == "~":
                                right = x
                                fill[1] = False
                                break
                        else:
                            right = x
                            fill[1] = False
                            break
                        # look in current space
                        if x in reservoir[wfs[wf][0]]:
                            if reservoir[wfs[wf][0]][x] == "#":
                                right = x-1
                                break
                    if right == None:
                        right = mmx[0]+1

                    if fill == [True, True]:
                        for xs in range(left, right+1):
                            reservoir[wfs[wf][0]][xs] = "~"
                        wfs[wf][0] -= 1
                    else:
                        for xs in range(left, right+1):
                            reservoir[wfs[wf][0]][xs] = "|"
                        clrwf.append(wf)
                        if left < mmx[0]:
                            mmx[0] = left
                        if right > mmx[1]:
                            mmx[1] = right
                        if fill[0] == False:
                            if not [wfs[wf][0], left] in addwf.values():
                                addwf[wfid] = [wfs[wf][0], left]
                                wfid += 1
                        if fill[1] == False:
                            if not [wfs[wf][0], right] in addwf.values():
                                addwf[wfid] = [wfs[wf][0], right]
                                wfid += 1
                else:
                    reservoir[wfs[wf][0]+1][wfs[wf][1]] = "|"
                    wfs[wf][0] += 1
            else:
                reservoir[wfs[wf][0]+1][wfs[wf][1]] = "|"
                wfs[wf][0] += 1
        else:
            if wfs[wf][0]+1 > mmy[1]:
                clrwf.append(wf)
                continue
            else:
                reservoir[wfs[wf][0]+1] = {}
                reservoir[wfs[wf][0]+1][wfs[wf][1]] = "|"
                wfs[wf][0] += 1
                    # clay is below the current water flow, check for walls left and right
                    # if there are two walls, fill between the walls with ~ and move the flow up
                    # if there are not walls or only one wall, fill the with | and creat flows
                    # over the edge of the clay floor
    for x in clrwf:
        wfs.pop(x)
    for y in addwf:
        wfs[y] = deepcopy(addwf[y])
    addwf.clear()
    clrwf.clear()
    if len(wfs) == 0:
        overflow = True
    #PrintGround()
    #input()

#PrintGround()
count = 0
drycount = 0
for ys in reservoir.keys():
    if ys < mmy[0] or ys > mmy[1]:
        continue
    for xs in reservoir[ys].keys():
        if reservoir[ys][xs] == "~" or reservoir[ys][xs] == "|":
            count += 1
        if reservoir[ys][xs] == "~":
            drycount += 1

print("No. tiles water reaches:> ", count)
print("No. tiles filled when spring dries up:> ", drycount)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)