from basicgraphs import graph

from utilities.graphIO import loadgraph, writeDOT


def refineColor(G: graph):
    nbs = generateNeighbourDict(G)
    a = dict()
    max = 0
    for v in G.V():
        nbsL = len(nbs[v])
        if nbsL > max:
            max = nbsL
        v.colornum = nbsL
        v.prevcol = nbsL
        if v.colornum not in a.keys():
            a[v.colornum] = set()
        a[v.colornum].add(v)

    print("a: " + str(a))
    print("max: " + str(max))
    # for i in a.keys():
    #     for u in a[i]:
    #         for v in a[i]:
    #             if u != v:
    #                 if not equal(u, v, nbs):
    #                     print("False")
    #                     v.prevcol, v.colornum = v.colornum, max + 1
    #                     max = v.colornum
    return G


def equal(u, v, nbs: dict()):
    print("u: " + str(u) + str(nbs[u]))
    print("v: " + str(v) + str(nbs[v]))
    if u.prevcol == v.prevcol and nbs[u] == nbs[v]:
        return True
    return False


def generateNeighbourDict(G: graph, directed=False):
    nbs = dict()
    for v in G.V():
        nbs[v] = set()
    for e in G.E():
        nbs[e.tail()].add(e.head())
        if not directed:
            nbs[e.head()].add(e.tail())
    return nbs


if __name__ == "__main__":
    G = loadgraph("colorref_smallexample_4_7.grl")
    # H = loadgraph("colorref_smallexample_4_16.grl")
    writeDOT(refineColor(G), "TestG.dot")
    # writeDOT(refineColor(H), "TestH.dot")
