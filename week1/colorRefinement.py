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

        #for each vertex u in G.V()
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

                    #Check if they are still "equal"
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


if __name__ == "__main__":
    g = loadgraph("./data/colorref_smallexample_4_16.grl")
    print(refineColors(g))
    graphIO.writeDOT(g, "output.dot")

