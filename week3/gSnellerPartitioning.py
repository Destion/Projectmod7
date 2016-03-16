from utilities.graphIO import loadgraph, writeDOT
from utilities.graphUtil import generateNeighbourList, disjointUnionMulti
from utilities.pythonex1 import createCycleGraph


def generatePartitions(G):
    neighbours = generateNeighbourList(G)
    p = []
    degrees = dict()
    for v in G.V():
        degree = len(neighbours[v])
        if degrees.get(degree, -1) == -1:
            degrees[degree] = {v}
        else:
            degrees[degree].add(v)

    for k in degrees:
        p.append(degrees[k])


    w = {0}
    while w:
        aN = w.pop()
        a = p[aN]
        for degree in degrees:
            nbs = set()
            for va in a:
                nbs |= neighbours[va]
            x = nbs | degrees[degree]

            for yN in {c for c in range(len(p)) if x&p[c] and p[c]-x}:
                y = p[yN]
                p[yN] = x&y
                p.append(y-x)
                if yN in w:
                    w.add(len(p)-1)
                else:
                    if len(x&y) <= len(y-x):
                        w.add(yN)
                    else:
                        w.add(len(p) - 1)
    return p

if __name__ == "__main__":
    gl = loadgraph("./../data/trees36.grl", readlist=True)
    # gl = [[disjointUnionMulti([createCycleGraph(3), createCycleGraph(3)]), createCycleGraph(7), createCycleGraph(6)]]
    i = 0
    p = generatePartitions(gl[0][0])
    for i in range(len(p)):
        for v in p[i]:
            v.colornum = i
    writeDOT(gl[0][0], "output.dot")
    print(p)