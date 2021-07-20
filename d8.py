import time
from copy import deepcopy
st = time.time()

inputfile = "input8.txt"

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
class Tnode:
    def __init__(self, id, children=[], meta=[]):
        self.id = id
        self.children = children
        self.meta = meta
        self.value = 0

inp = readinput()
#inp = splitinput()
inp = inp[0].split(" ")
ent = []
for x in inp:
    ent.append(int(x))

idno = 0
def traverseTree(prev, rawnode):
    global idno
    idno += 1
    #print(idno, rawnode)
    nochil = rawnode[0]
    nometa = rawnode[1]
    node = Tnode(idno, [], [])
    prev.children.append(node)
    nodelen = 2
    for _ in range(nochil):
        nodelen += traverseTree(node, deepcopy(rawnode[nodelen:-(nometa)]))
    if nochil == 0:
        node.meta = deepcopy(rawnode[2:(2+nometa)])
    else:
        node.meta = deepcopy(rawnode[nodelen:(nodelen+nometa)])
    return nodelen + nometa

nochil = ent[0]
nometa = ent[1]
tree = Tnode(idno, [], deepcopy(ent[-(nometa):]))
nodelen = 2
for b in range(nochil):
    nodelen += traverseTree(tree, deepcopy(ent[nodelen:-(nometa)]))
nodelen += nometa

metasum = sum(tree.meta)
def summeta(node):
    nsum = 0
    nsum += sum(node.meta)
    #input()
    for n in node.children:
        nsum += summeta(n)
    if len(node.children) == 0:
        node.value = nsum
    else:
        for i in node.meta:
            if i > 0 and i <= len(node.children):
                node.value += node.children[i-1].value
    #print(node.id, node.meta, node.value)
    return nsum

#print(tree.id, tree.meta)
for node in tree.children:
    #print(node.id)
    metasum += summeta(node)
for i in tree.meta:
    if i > 0 and i <= len(tree.children):
        tree.value += tree.children[i-1].value
print(metasum)
print(tree.value)


#print(tree.id, tree.children, tree.meta)
#print(nodelen)
## Solve problem



## Print runtime
et = time.time()
if (et - st) < 1:
    rt = str(round((et - st) * 1000,3)) + "ms"
else:
    rt = str(round(et - st,3)) + "s"
print("Runtime:> ", rt)