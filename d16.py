import time
from copy import deepcopy
st = time.time()

inputfile = "input16.txt"

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
#inp = readinput()
inp = splitinput()

tests = []
prog = []
## Solve problem
for x in inp:
    if len(x) == 3:
        tests.append(x)
    else:
        prog = deepcopy(x)

#print(tests)
#print(prog)

def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]
    return deepcopy(reg)

def addi(reg, a, b, c):
    reg[c] = reg[a] + b
    return deepcopy(reg)

def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]
    return deepcopy(reg)

def muli(reg, a, b, c):
    reg[c] = reg[a] * b
    return deepcopy(reg)

def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]
    return deepcopy(reg)

def bani(reg, a, b, c):
    reg[c] = reg[a] & b
    return deepcopy(reg)

def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]
    return deepcopy(reg)

def bori(reg, a, b, c):
    reg[c] = reg[a] | b
    return deepcopy(reg)

def setr(reg, a, b, c):
    reg[c] = reg[a]
    return deepcopy(reg)

def seti(reg, a, b, c):
    reg[c] = a
    return deepcopy(reg)

def gtir(reg, a, b, c):
    if a > reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return deepcopy(reg)

def gtri(reg, a, b, c):
    if reg[a] > b:
        reg[c] = 1
    else:
        reg[c] = 0
    return deepcopy(reg)

def gtrr(reg, a, b, c):
    if reg[a] > reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return deepcopy(reg)

def eqir(reg, a, b, c):
    if a == reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return deepcopy(reg)

def eqri(reg, a, b, c):
    if reg[a] == b:
        reg[c] = 1
    else:
        reg[c] = 0
    return deepcopy(reg)

def eqrr(reg, a, b, c):
    if reg[a] == reg[b]:
        reg[c] = 1
    else:
        reg[c] = 0
    return deepcopy(reg)

oplist = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

opcodes = {}
simps = 0
for s in tests:
    gtthree = 0
    rea = [int(a) for a in s[0][9:-1].split(", ")]
    ops = [int(a) for a in s[1].split(" ")]
    res = [int(a) for a in s[2][9:-1].split(", ")]

    for o in oplist:
        if o(deepcopy(rea), ops[1], ops[2], ops[3]) == res:
            if not ops[0] in opcodes:
                opcodes[ops[0]] = set()
            opcodes[ops[0]].add(o)
            gtthree += 1
    
    if gtthree >= 3:
        simps += 1

print("Part 1:> ", simps)

unsorted = list(opcodes.keys())

while len(unsorted) > 0:
    for x in unsorted:
        if len(opcodes[x]) == 1:
            s = next(iter(opcodes[x]))
            for y in opcodes:
                if y == x:
                    continue
                opcodes[y].discard(s)
            unsorted.pop(unsorted.index(x))

for x in opcodes:
    opcodes[x] = opcodes[x].pop()

rea = [0, 0, 0, 0]
for l in prog:
    ops = [int(a) for a in l.split(" ")]
    rea = opcodes[ops[0]](deepcopy(rea), ops[1], ops[2], ops[3])

print("Part 2:> ", rea[0])


## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)