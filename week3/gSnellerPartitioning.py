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

    w = set(range(len(p)-1))
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


def writeColors(partitions):
    for i in range(len(partitions)):
        for v in partitions[i]:
            v.colornum = i


if __name__ == "__main__":
    from utilities.graphIO import loadgraph, writeDOT
    from trees.automorphismsCounter import countTreeAutomorphisms

    gl = loadgraph("./../data/bigtrees2.grl", readlist=True)
    # gl = [[disjointUnionMulti([createCycleGraph(3), createCycleGraph(3)]), createCycleGraph(7), createCycleGraph(6)]]
    i = 0
    g = gl[0][1]
    #g = loadgraph("./../data/threepaths10240.gr")

    p = generatePartitions(g)
    print(p)
    writeColors(p)
    automorphisms = 1
    for part in p:
        automorphisms *= len(part)
    print("Fout : ", automorphisms)
    print("Goed?: ", countTreeAutomorphisms(g))
    writeDOT(g, "output.dot")
