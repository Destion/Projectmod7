import graphIO
from basicgraphs import graph
from graphIO import loadgraph
from graphUtil import disjointUnion


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

    # define a number that gives a color that has not yet been chosen
    nextColor = 0
    # Fill a with colors related to the degree of the vertex
    for v in G.V():
        a[v] = len(neighbours[v])
        nextColor = max(len(neighbours[v]) + 1, nextColor)

    # while the colors still change after an iteration
    while aPrev != a:
        aPrev = a
        a = dict()

        # for each vertex u in G.V()
        for i in range(len(G.V())):
            u = G.V()[i]

            # initialize nc, the new color of u
            nc = a.get(u, aPrev[u])

            # create a set "same" that will contain all vertices v that are "equal" to the current vertex u
            same = set()

            # for every unchecked vertex v
            for v in G.V()[i + 1:]:

                # if the vertices were "equal" and not exactly the same
                if u != v and aPrev[u] == aPrev[v]:

                    # Check if they are still "equal"
                    if not haveSameNeighbours(u, v, neighbours, aPrev):

                        # they are not equal anymore, if we haven't updated nc already, do it now
                        if nc == aPrev[u]:
                            nc = nextColor
                            nextColor += 1
                    else:
                        # they are still equal, add the vertex to our "same" set
                        same.add(v)

            # update the a[v] of every v in same
            for v in same:

                # If nc and a[v] (or the previous a[v]) differ, change a[v]
                if nc != a.get(v, aPrev[v]):
                    a[v] = nc
            a[u] = nc

    # set the colornums
    for v in a:
        v.colornum = a[v]

    return a


def areIsomorph(G1: graph, G2: graph):
    # This function requires that the disjointUnion places all vertices of G1 after or before all vertices of G2
    if len(G1.V()) != len(G2.V()) or len(G1.E()) != len(G2.E()):
        return False
    G = disjointUnion(G1, G2)
    a = refineColors(G)

    # the colordict will be filled with all the colors as keys and a value that represents the status:
    # 0 = in second graph, but not first, 1 = in first graph, 2 = in first and second graph
    colorDict = dict()
    i = 0
    for k in G.V():
        v = a[k]
        if i >= len(G1.V()):
            if colorDict.get(v, 0) != 0:
                colorDict[v] = 2
            else:
                colorDict[v] = 0
        else:
            colorDict[v] = 1
        i += 1


    for c in colorDict:
        v = colorDict[c]
        if v < 2:
            return False

    return True

def getAllIsomorphisms(graphList):
    groups = [[graphList[0]]]
    for g in graphList[1:]:
        placed = False
        for group in groups:
            if areIsomorph(g, group[0]):
                group.append(g)
                placed = True
                break
        if not placed:
            groups.append([g])
    return groups

if __name__ == "__main__":
    gl = loadgraph("./data/colorref_smallexample_6_15.grl", readlist=True)
    for group in getAllIsomorphisms(gl[0]):
        print("Group with size: ", len(group))
