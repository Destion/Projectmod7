from basicgraphs import graph

"""
This file defines useful functions for graphs that are not included in basicGraphs
"""


def generateNeighbourList(G: graph, directed=False, inclists=False):
    """
    Generates a neighbour or inclist so the respective functions don't have to be called constantly (they are very slow)
    :param G: the graph
    :param directed: whether the graph is directed. In this case only outgoing edges will be added
    :param inclists: True when you want the inclist, false or not assigned if you want the neighbourlist
    :return: neighbourlist or inclist of graph g as a dict with key v (vertex) as value a set of vertices or edges
    """
    neighbours = dict()
    inclistsD = dict()
    for v in G.V():
        neighbours[v] = set()
        inclistsD[v] = set()
    for e in G.E():
        neighbours[e.tail()].add(e.head())
        inclistsD[e.tail()].add(e)
        if not directed:
            neighbours[e.head()].add(e.tail())
            inclistsD[e.head()].add(e)
    if inclists:
        return inclistsD
    else:
        return neighbours


def disjointUnion(g: graph, h: graph):
    f = graph(len(g.V()) + len(h.V()))
    combinedList = g.V() + h.V()
    for i in range(len(combinedList)):
        v = combinedList[i]
        for e in v.inclist():
            if e.tail() == v:
                f.addedge(f[i], f[combinedList.index(e.head())])

    return f


def disjointUnionMulti(graphList):
    f = graph(sum([len(g.V()) for g in graphList]))
    inclist = dict()
    combinedList = [v for g in graphList for v in g]
    for g in graphList:
        inclist.update(generateNeighbourList(g, inclists=True))
    for i in range(len(combinedList)):
        v = combinedList[i]
        for e in inclist[v]:
            if e.tail() == v:
                f.addedge(f[i], f[combinedList.index(e.head())])

    return f
