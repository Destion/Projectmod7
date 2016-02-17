from basicgraphs import graph
from graphIO import loadgraph, writeDOT


def refineColor(G):
    nbs = generateNeighbourDict(G)
    for v in range(len(G.V())):
        G.V()[v].colornum = len(nbs[G.V()[v]])

    return G


def generateNeighbourDict(G: graph, directed=False):
    nbs = dict()
    for v in G.V():
        nbs[v] = set()
    for e in G.E():
        nbs[e.tail()].add(e.head())
        if not directed:
            nbs[e.head()].add(e.tail())
    print(nbs)
    return nbs


if __name__ == "__main__":
    G = loadgraph("colorref_smallexample_4_7.grl")
    H = loadgraph("colorref_smallexample_4_16.grl")
    writeDOT(refineColor(G), "TestG.dot")
    writeDOT(refineColor(H), "TestH.dot")
