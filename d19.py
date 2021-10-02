import time
from copy import deepcopy
st = time.time()

inputfile = "input19.txt"

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
class OpComp():

    def __init__(self, ip, instr, mode=0):
        self.reg = [0, 0, 0, 0, 0, 0]
        self.ip = int(ip)
        self.instr = deepcopy(instr)
        if mode == 1:
            self.reg[0] = 1
        self.history = []

    def RunComp(self):

        while self.reg[self.ip] >= 0 and self.reg[self.ip] < len(self.instr):
            inst = self.instr[self.reg[self.ip]]
            com = inst.split(" ")
            i, a, b, c = com[0], int(com[1]), int(com[2]), int(com[3])

            # sum of multiples of value in reg[3]
            if self.reg[self.ip] == 3:
                t = self.reg[3]
                halft = int(t / 2 + 1)
                sm = 0
                for x in range(1, halft+1):
                    if t % x == 0:
                        sm += x         
                sm += t
                self.reg[0] = sm
                self.reg[self.ip] = 16
                continue

            if i == "addr":
                self.reg[c] = self.reg[a] + self.reg[b]

            if i == "addi":
                self.reg[c] = self.reg[a] + b

            if i == "mulr":
                self.reg[c] = self.reg[a] * self.reg[b]

            if i == "muli":
                self.reg[c] = self.reg[a] * b

            if i == "banr":
                self.reg[c] = self.reg[a] & self.reg[b]

            if i == "bani":
                self.reg[c] = self.reg[a] & b

            if i == "borr":
                self.reg[c] = self.reg[a] | self.reg[b]

            if i == "bori":
                self.reg[c] = self.reg[a] | b

            if i == "setr":
                self.reg[c] = self.reg[a]

            if i == "seti":
                self.reg[c] = a

            if i == "gtir":
                if a > self.reg[b]:
                    self.reg[c] = 1
                else:
                    self.reg[c] = 0

            if i == "gtri":
                if self.reg[a] > b:
                    self.reg[c] = 1
                else:
                    self.reg[c] = 0

            if i == "gtrr":
                if self.reg[a] > self.reg[b]:
                    self.reg[c] = 1
                else:
                    self.reg[c] = 0

            if i == "eqir":
                if a == self.reg[b]:
                    self.reg[c] = 1
                else:
                    self.reg[c] = 0

            if i == "eqri":
                if self.reg[a] == b:
                    self.reg[c] = 1
                else:
                    self.reg[c] = 0

            if i == "eqrr":
                if self.reg[a] == self.reg[b]:
                    self.reg[c] = 1
                else:
                    self.reg[c] = 0

            self.reg[self.ip] += 1

            #print(inst, self.reg)
        #print(inst, self.reg)
        return(self.reg[0])

ip = inp.pop(0)
comp = OpComp(ip[-1], inp)
res = comp.RunComp()
print("Result of Part 1:>", res)

comp2 = OpComp(ip[-1], inp, 1)
res = comp2.RunComp()
print("Result of Part 2:>", res)

## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)