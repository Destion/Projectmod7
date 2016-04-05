import time

from utilities.graphUtil import generateNeighbourList, disjointUnionMulti, isConnected, isTree
from utilities.pythonex1 import createCycleGraph

def generatePfromColors(G):
    p = []
    colors = dict()
    for v in G.V():
        if v.colornum in colors.keys():
            colors[v.colornum].add(v)
        else:
            colors[v.colornum] = {v}
    keys = list(colors.keys())
    for key in keys:
        p.append(colors[key])
    return p


def generatePartitions(G, usecolors=False):
    neighbours = generateNeighbourList(G)
    p = []
    degrees = dict()
    for v in G.V():
        degree = len(neighbours[v])
        if degrees.get(degree, -1) == -1:
            degrees[degree] = {v}
        else:
            degrees[degree].add(v)

    if usecolors:
        p = generatePfromColors(G)
    else:
        for k in degrees:
            p.append(degrees[k])

    w = set(range(len(p)))
    while w:
        # print(w)
        aN = w.pop()
        a = p[aN]
        for color in p:
            if color == a:
                continue
            nbs = set()
            for va in a:
                nbs |= neighbours[va]
            x = nbs | color
            for yN in range(len(pSplit)):
                if pSplit[yN] != color and len(p[yN]) > 1:
                    y = pSplit[yN]
                    both = x&y
                    ynotx = y-x
                    if both and ynotx:
                        p[yN] = both
                        p.append(ynotx)
                        if yN in w:
                            w.add(len(p)-1)
                        else:
                            if len(both) <= len(ynotx):
                                w.add(yN)
                            else:
                                w.add(len(p) - 1)
    return p


def generatePartitionsv2(G, usecolors=False):
    neighbours = generateNeighbourList(G)
    p = []
    pSplit = []
    degrees = dict()
    for v in G.V():
        degree = len(neighbours[v])
        if degrees.get(degree, -1) == -1:
            degrees[degree] = {v}
        else:
            degrees[degree].add(v)

    if usecolors:
        p = generatePfromColors(G)
        pSplit = generatePfromColors(G)
    else:
        for k in degrees:
            p.append(degrees[k])
            pSplit.append(degrees[k])

    w = set(range(len(p)))
    while w:
        #print("w: ", w)
        #print("wl: ", [(c, len(p[c])) for c in w])
        aN = w.pop()
        a = p[aN]
        nbs = set()
        for va in a:
            nbs |= neighbours[va]
        # print("nbs: ", nbs)
        for color in pSplit:
            x = nbs & color
            # print("nbs & color: ", x)
            if x:
                for yN in range(len(p)):
                    if len(p[yN]) > 1:
                        y = p[yN]
                        both = x&y
                        ynotx = y-x
                        if both and ynotx:
                            p[yN] = both
                            p.append(ynotx)
                            if yN in w:
                                w.add(len(p)-1)
                            else:
                                if len(both) <= len(ynotx):
                                    w.add(yN)
                                else:
                                    w.add(len(p) - 1)
    return p


def writeColors(partitions):
    for i in range(len(partitions)):
        for v in partitions[i]:
            v.colornum = i


if __name__ == "__main__":
    from utilities.graphIO import loadgraph, writeDOT
    from trees.automorphismsCounter import countTreeAutomorphismsLS, countTreeAutomorphismsRS

    gl = loadgraph("./../data/products72.grl", readlist=True)
    #gl = [[disjointUnionMulti([createCycleGraph(3), createCycleGraph(3)]), createCycleGraph(7), createCycleGraph(6)]]
    i = 0
    g = gl[0][0]
    g = loadgraph("./../data/threepaths10240.gr")
    t = time.time()
    p = generatePartitionsv2(g)
    print(time.time() - t)
    print(p)
    writeColors(p)
    print("Goed?: ", countTreeAutomorphismsLS(g))
    print("Goed?: ", countTreeAutomorphismsRS(g))


    writeDOT(g, "output.dot")
