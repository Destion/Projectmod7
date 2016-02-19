import graphIO
from basicgraphs import graph
from graphIO import loadgraph
from graphUtil import disjointUnionMulti, generateNeighbourList


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


def areIsomorph(G: graph, i1, i2, l1, l2, a):
    """

    :param G: The graph containing a disjoint union of all graphs
    :param i1: The index of the first vertex of G1 in G
    :param i2: The index of the first vertex of G2 in G
    :param l1: The length of G1.V()
    :param l2: The length of G2.V()
    :param a: The colors of G.V() returned by refineColors()
    :return: Whether G1 an G2 are isomorph according to G and a
    """

    # the colordict will be filled with all the colors as keys and a value that represents the status:
    # 0 = in second graph, but not first, 1 = in first graph, 2 = in first and second graph

    G1v = G.V()[i1: i1 + l1]
    G2v = G.V()[i2: i2 + l2]

    colorDict = dict()
    i = 0
    for k in G1v + G2v:
        v = a[k]
        if i >= l1:
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
    groupStartIndices = [0]
    startIndices = [0]
    lenghts = [len(graphList[0].V())]

    for g in graphList:
        startIndices.append(startIndices[-1] + lenghts[-1])
        lenghts.append(len(g.V()))

    G = disjointUnionMulti(graphList)
    a = refineColors(G)
    i = 1
    for g in graphList[1:]:
        placed = False
        for groupI in range(len(groups)):
            if areIsomorph(G, startIndices[i], startIndices[groupStartIndices[groupI]],
                           lenghts[i], lenghts[groupStartIndices[groupI]], a):
                groups[groupI].append(g)
                placed = True
                break
        if not placed:
            groups.append([g])
            groupStartIndices.append(i)
        i += 1
    return groups


if __name__ == "__main__":
    gl = loadgraph("./data/colorref_largeexample_6_960.grl", readlist=True)
    for group in getAllIsomorphisms(gl[0]):
        print("Group with size: ", len(group))
