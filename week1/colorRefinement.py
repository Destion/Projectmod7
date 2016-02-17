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
    print(a, v1, v2)
    return [a[v] for v in neighbours[v1]] == [a[v] for v in neighbours[v2]]


def refineColors(G: graph):
    a = dict()
    aPrev = dict()
    neighbours = generateNeighbourList(G)
    nextColor = 0
    for v in G.V():
        a[v] = len(neighbours[v])
        nextColor = max(len(neighbours[v]), nextColor) + 1

    while aPrev != a:
        print("Loop!")
        aPrev = a
        a = dict()
        for u in G.V():
            for v in G.V():
                if u != v and aPrev[u] == aPrev[v]:
                    if not haveSameNeighbours(u, v, neighbours, aPrev):
                        print("Waaaahhhh")
                        print(nextColor)
                        a[u] = nextColor
                        a[v] = aPrev[v]
                        nextColor += 1
                    else:
                        a[v] = aPrev[v]
                        a[u] = aPrev[u]
                else:
                    a[v] = aPrev[v]
                    a[u] = aPrev[u]
    print("\n\n\n\nDONE:")
    print(a)
    for v in a:
        v.colornum = a[v]

    return a


if __name__ == "__main__":
    g = loadgraph("./data/colorref_smallexample_4_16.grl")
    print(refineColors(g))
    graphIO.writeDOT(g, "output.dot")

