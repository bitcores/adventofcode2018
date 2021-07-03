import time
st = time.time()

inputfile = "input5.txt"

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
chem = inp[0]

def shim(c):
    for x in range(65,91):
        c = c.replace(chr(x)+chr(x+32), "")
        c = c.replace(chr(x+32)+chr(x), "")
    return c

while True:
    sl = len(chem)
    chem = shim(chem)
    if len(chem) == sl:
        break

print("Part 1 result:> ", len(chem))

shortest = 999999999
for x in range(65,91):
    chem2 = inp[0]
    chem2 = chem2.replace(chr(x), "")
    chem2 = chem2.replace(chr(x+32), "")
    
    while True:
        sl = len(chem2)
        chem2 = shim(chem2)
        if len(chem2) == sl:
            break

    if len(chem2) < shortest:
        shortest = len(chem2)

print("Part 2 result:> ", shortest)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)