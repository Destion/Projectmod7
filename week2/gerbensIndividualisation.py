import graphIO
from basicgraphs import graph
from graphIO import loadgraph
from week1.colorRefinement import addToRevDict, refineColorsv2, getAllIsomorphisms


def refineFurther(groups, G: graph):
    newGroups = []
    for group in groups:
        newGroups += refineGroup(group)
    return newGroups, G

def resetColors(G: graph, oldColors):
    for v in G.V():
        v.colornum = oldColors[G][v]

def refineGroup(group):
    # graph -> color -> set(v1 = v2 = ... = vn)
    bijectionCandidates = dict()

    # graph -> vertex -> color
    currentColors = dict()

    nextColor = 0
    for g in group:
        for v in g.V():
            addToRevDict(bijectionCandidates[g], v.colornum, v)
            currentColors[g][v] = v.colornum
            if v.colornum > nextColor:
                nextColor = v.colornum
        keys = bijectionCandidates[g].keys()
        for colornum in keys:
            if len(bijectionCandidates[g][colornum]) == 1:
                del bijectionCandidates[g][colornum]

    bestColor = bijectionCandidates[0].keys()[0]
    for color in bijectionCandidates[0].keys():
        if len(bijectionCandidates[0][color]) > len(bijectionCandidates[0][bestColor]):
            bestColor = color

    nextColor += 1
    color = bestColor
    for g1 in group:

        v1 = bijectionCandidates[g1][color].pop()
        bijectionCandidates[g1][color].add(v1)
        for g2 in group:
                for v2 in bijectionCandidates[g2][color]:
                    v1.colornum, v2.colornum = nextColor, nextColor
                    print(getAllIsomorphisms([g1, g2]))
                resetColors(g2, currentColors)

        resetColors(g1, currentColors)

if __name__ == "__main__":
    gl = loadgraph("./../data/cographs1.grl", readlist=True)

    i = 0
    groups, G = getAllIsomorphisms(gl[0])
    groups, G = refineFurther(groups, G)