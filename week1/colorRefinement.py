import graphIO
from basicgraphs import graph
from graphIO import loadgraph
from graphUtil import disjointUnionMulti, generateNeighbourList


def haveSameNeighbours(v1, v2, neighbourColors):

    if len(neighbourColors[v1]) != len(neighbourColors[v2]):
        # if the degree is not equal, return False imediately
        return False
    return neighbourColors[v1] == neighbourColors[v2]


def getNeighbourColors(neighbours, a):

    # init a new dict nbColors (neighbour colors)
    nbColors = dict()

    # this for loop loops over every vertex g (don't be disctracted by the neighbours part yet!)
    for g in neighbours:
        nbColors[g] = dict()

        # loop over every neighbour of g and add its color to our dictionary of neighbour colors
        # every vertex g has a value in the nbColor dict, with as value a dict that acts like a multiset
        # a vertex g with 3 neighbours, 2 with color "1" and 1 with color "3" will give:
        # nbColors[g] = {1: 2, 3: 1}
        for nb in neighbours[g]:
            nbColors[g][a[nb]] = nbColors[g].get(a[nb], 0) + 1
    return nbColors


def addToRevDict(d: dict, k, e):
    # a fast function operating on a dict d with a key k and as value a set
    # this function will create a set containing e as value for key k if key k did not have a value in d yet
    # if d already had a key k with as value a set, the function will add e to that set
    if d.get(k, None) is None:
        d[k] = {e}
    else:
        d[k].add(e)

# depricated!!!
def refineColors(G: graph):
    a = dict()
    aPrev = dict()
    neighbours = generateNeighbourList(G)

    # define a number that gives a color that has not yet been chosen
    nextColor = 0
    # Fill a with colors related to the degree of the vertex
    for v in G.V():
        a[v] = len(neighbours[v])
        nextColor = max(a[v] + 1, nextColor)

    # while the colors still change after an iteration
    while aPrev != a:
        aPrev = a
        a = dict()
        nbColors = getNeighbourColors(neighbours, aPrev)
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
                    if not haveSameNeighbours(u, v, nbColors):

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


def refineColorsv2(G: graph):

    # a is a dict that contains a vertex as key and a color as value
    a = dict()

    # the old a, from the previous iteration
    aPrev = dict()

    # aRev (a reversed) contains a color as key and a set of vertices that have that color as value
    aRev = dict()

    # the a reversed dict of the previous iteration
    aRevPrev = dict()

    # generate a dict of vertex -> vertices that contains all the neighbours of the key vertex
    neighbours = generateNeighbourList(G)

    # define a number that gives a color that has not yet been chosen
    nextColor = 0

    # Fill a with colors related to the degree of the vertex
    for v in G.V():

        # color of v = the degree of v (number of neighbours)
        a[v] = len(neighbours[v])

        addToRevDict(aRev, a[v], v)

        # make sure nextColor is always higher than the highest color that was already used
        nextColor = max(a[v] + 1, nextColor)

    # while the colors still change after an iteration
    while aPrev != a:

        # set the Prev dicts to the previous values of a and aRev and reset a and aRev
        aPrev = a
        aRevPrev = aRev
        a = dict()
        aRev = dict()

        nbColors = getNeighbourColors(neighbours, aPrev)

        # pus all the vertices that we have already refined in the set done so we won't have to check them again
        done = set()
        # for each vertex u in G.V()
        for u in G.V():

            # if u has already been refined earlier in this iteration, skip it now
            if u in done:
                continue

            # initialize nc, the new color of u
            nc = a.get(u, aPrev[u])

            # create a set "same" that will contain all vertices v that are "equal" to the current vertex u
            same = set()

            # for every vertex v that was equal
            for v in aRevPrev[aPrev[u]]:

                # if the vertices were "equal" and not exactly the same
                if u != v:

                    # Check if they are still "equal"
                    if not haveSameNeighbours(u, v, nbColors):

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
                    addToRevDict(aRev, nc, v)
                    done.add(v)

            a[u] = nc
            addToRevDict(aRev, nc, u)

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

    # these lists are the parts of the full vertex list G.V() that belonged to the graphs we are testing
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
    # Make a list of groups
    groups = [[graphList[0]]]

    # these lists hold indices of our graphs in the vertex list of our union graph and the lengths of the vertex lists
    groupStartIndices = [0]
    startIndices = [0]
    lenghts = [len(graphList[0].V())]

    for g in graphList:
        startIndices.append(startIndices[-1] + lenghts[-1])
        lenghts.append(len(g.V()))

    # create one gaint graph containing all the graphs in our graphlist
    G = disjointUnionMulti(graphList)

    # execute the refineColors function on our union graph
    a = refineColorsv2(G)
    i = 1

    # fill the groups based on our new color data
    for g in graphList[1:]:

        # this boolean indicates whether the current graph has been placed in a group
        placed = False
        for groupI in range(len(groups)):
            if areIsomorph(G, startIndices[i], startIndices[groupStartIndices[groupI]],
                           lenghts[i], lenghts[groupStartIndices[groupI]], a):
                groups[groupI].append(g)
                placed = True
                break
        # if our graph is not yet placed, it belongs to a new group
        if not placed:
            groups.append([g])
            groupStartIndices.append(i)
        i += 1
    return groups, G


if __name__ == "__main__":
    gl = loadgraph("./data/colorref_largeexample_6_960.grl", readlist=True)

    i = 0
    groups, G = getAllIsomorphisms(gl[0])
    graphIO.writeDOT(G, "./output.dot")
    for group in groups:
        print("Group with size: ", len(group))
        graphIO.writeDOT(disjointUnionMulti(group), "./output%i.dot" % i)
        i += 1
