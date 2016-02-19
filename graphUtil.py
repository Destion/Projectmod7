from basicgraphs import graph

"""
This file defines useful functions for graphs that are not included in basicGraphs
"""


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
    f = graph(sum([len(g) for g in graphList]))
    combinedList = [v for g in graphList for v in g]
    for i in range(len(combinedList)):
        v = combinedList[i]
        for e in v.inclist():
            if e.tail() == v:
                f.addedge(f[i], f[combinedList.index(e.head())])

    return f
