import graphIO
from basicgraphs import graph
from graphIO import loadgraph


def generateNeighbourList(G: graph, directed=False):
    neighbours = dict()
    for v in G.V():
        neighbours[v] = set()
    for e in G.E():
        neighbours[e.tail()].add(e.head())
        if not directed:
            neighbours[e.head()].add(e.tail())
    return neighbours

def haveSameNeighbours(v1, v2, neighbours, a):
    if len(neighbours[v1]) != len(neighbours[v2]):
        return False
    return sorted([a[v] for v in neighbours[v1]]) == sorted([a[v] for v in neighbours[v2]])


def refineColors(G: graph):
    a = dict()
    aPrev = dict()
    neighbours = generateNeighbourList(G)
    nextColor = 0
    for v in G.V():
        a[v] = len(neighbours[v])
        nextColor = max(len(neighbours[v]) + 1, nextColor)

    while aPrev != a:
        aPrev = a
        a = dict()
        for i in range(len(G.V())):
            u = G.V()[i]
            nc = a.get(u, aPrev[u])
            same = set()
            for v in G.V()[i + 1:]:
                if u != v and aPrev[u] == aPrev[v]:
                    if not haveSameNeighbours(u, v, neighbours, aPrev):
                        if nc == aPrev[u]:
                            nc = nextColor
                            nextColor += 1
                    else:
                        same.add(v)
            for v in same:

                if nc != a.get(v, aPrev[v]):

                    a[v] = nc

            a[u] = nc

    for v in a:
        v.colornum = a[v]

    return a


if __name__ == "__main__":
    g = loadgraph("./data/colorref_smallexample_4_16.grl")
    print(refineColors(g))
    graphIO.writeDOT(g, "output.dot")

