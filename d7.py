import time
st = time.time()

inputfile = "input7.txt"

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
bsteptime = 60
steptime = -(ord("A"))+1
workers = 5
working = {}
steps = set()
children = {}
deps = {}
for l in inp:
    d = l[5]
    s = l[-12]
    steps.add(d)
    steps.add(s)
    if not s in deps:
        deps[s] = []
    deps[s].append(d)
    if not d in children:
        children[d] = []
    children[d].append(s)

#print(steps)
#print(deps)
#print(children)
avail = []
avail2 = []

for x in steps:
    if not x in deps:
        #print("starting step ", x)
        avail.append(x)
        avail2.append(x)

corder = ""

def chkfulfildeps(co, d):
    tester = []
    for x in deps[d]:
        if x in co:
            tester.append(True)
        else:
            tester.append(False)
    return (tester.count(True) == len(deps[d]))

while len(avail) > 0:
    avail.sort()
    t = 0
    while t < len(avail):
        if avail[t] in corder:
            print("Anomolous error")
            print(avail)
            print(corder)
            avail.clear()
            break
        if not avail[t] in deps or chkfulfildeps(corder, avail[t]):
            corder += avail[t]
            if avail[t] in children:
                for y in children[avail[t]]:
                    if not y in avail:
                        avail.append(y)
            avail.pop(t)
            break
        t += 1
    
    #print(avail)
    #print(corder)
    #input()

print("Step order:> ", corder)

corder2 = ""
timer = -1
#print(avail2)
while len(avail2) > 0 or len(working) > 0:
    timer += 1
    cleanup = []
    for task in working:
        working[task] -= 1

        if working[task] == 0:
            corder2 += task
            cleanup.append(task)
    
    for x in cleanup:
        working.pop(x)
        if x in children:
            for y in children[x]:
                if not y in avail2:
                    avail2.append(y)
    cleanup.clear()

    if len(working) < workers:
        avail2.sort()
        rmavail = []
        for a in avail2:
            if a in corder2:
                print("Anomolous error")
                print(avail2)
                print(corder)
                avail2.clear()
                break
            if not a in deps or chkfulfildeps(corder2, a):
                if len(working) < workers:
                    working[a] = bsteptime + steptime + ord(a)
                    rmavail.append(a)
                else:
                    break
        for z in rmavail:
            avail2.pop(avail2.index(z))
                
    #print(working)
    #print(timer, corder2)
    #input()

print("Step order:> ", corder2, " in ", timer, " seconds.")

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)