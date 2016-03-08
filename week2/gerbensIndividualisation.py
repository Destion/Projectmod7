from utilities.basicgraphs import graph
from utilities.graphUtil import disjointUnionMulti
from utilities.pythonex1 import createCycleGraph
from utilities import graphIO
from utilities.graphIO import loadgraph
from week1.colorRefinement import addToRevDict, getAllIsomorphisms


def refineFurther(groups):
    newGroups = []
    for group in groups:
        if len(group) == 1 or hasNoDuplicateColors(group):
            newGroups.append(group)
            continue
        newGroup = group
        noDuplicates = True
        newGroup = refineGroup(newGroup)
        print(len(newGroup))
        for tGroup in newGroup:
            noDuplicates = noDuplicates and hasNoDuplicateColors(tGroup)
            if not noDuplicates:
                newGroup = refineFurther(newGroup)
                break
        newGroups += newGroup
    return newGroups


def resetColors(G: graph, oldColors):
    for v in G.V():
        v.colornum = oldColors[G][v]


def extractColors(g1, g2, earlierColoring = None):

    if earlierColoring is not None:
        pass


def hasNoDuplicateColors(group):
    for g in group:
        colors = set()
        for v in g.V():
            if v.colornum not in colors:
                colors.add(v.colornum)
            else:
                return False
    return True

def refineGroup(group):
    # graph -> color -> set(v1 = v2 = ... = vn)
    bijectionCandidates = dict()

    # graph -> vertex -> color
    currentColors = dict()

    nextColor = 0
    for g in group:
        bijectionCandidates[g] = dict()
        currentColors[g] = dict()
        for v in g.V():
            addToRevDict(bijectionCandidates[g], v.colornum, v)
            currentColors[g][v] = v.colornum
            if v.colornum > nextColor:
                nextColor = v.colornum
        keys = list(bijectionCandidates[g].keys())
        for colornum in keys:
            if len(bijectionCandidates[g][colornum]) == 1:
                bijectionCandidates[g].pop(colornum)
    if len(bijectionCandidates[group[0]].keys()) == 0:
        return group
    bestColor = list(bijectionCandidates[group[0]].keys())[0]
    for color in bijectionCandidates[group[0]].keys():
        if len(bijectionCandidates[group[0]][color]) > len(bijectionCandidates[group[0]][bestColor]):
            bestColor = color

    nextColor += 1
    done = set()
    color = bestColor
    print("BestColor: ", bestColor)
    newGroups = []
    for g1 in group:
        if g1 in done:
            continue
        done.add(g1)
        newGroups.append([g1])
        v1 = bijectionCandidates[g1][color].pop()
        bijectionCandidates[g1][color].add(v1)
        print(currentColors)
        for g2 in group:
            if g2 not in done:
                for v2 in bijectionCandidates[g2][color]:
                    print(v1, v2)
                    print(bijectionCandidates[g1], bijectionCandidates[g2])
                    resetColors(g1, currentColors)
                    resetColors(g2, currentColors)
                    v1.colornum, v2.colornum = nextColor, nextColor
                    # graphIO.writeDOT(disjointUnionMulti([g1, g2], holdColor=True ), "./outputUnion.dot")
                    iets, G = getAllIsomorphisms([g1, g2], True)

                    if v1.colornum == v2.colornum:
                        newGroups[-1].append(g2)
                        done.add(g2)
                        graphIO.writeDOT(G, "./outputIsomorphisms.dot")
                        print("Found bijection", v1, v2)
                        #resetColors(g1, currentColors)
                        #resetColors(g2, currentColors)
                        break
                    else:
                        resetColors(g1, currentColors)
                        resetColors(g2, currentColors)



    return newGroups

if __name__ == "__main__":
    gl = loadgraph("./../data/wheelstar12.grl", readlist=True)
    gl = [[createCycleGraph(3), createCycleGraph(3), createCycleGraph(6)]]
    i = 0
    groups, G = getAllIsomorphisms(gl[0])
    groups = refineFurther(groups)
    print([len(group) for group in groups])
    graphIO.writeDOT(disjointUnionMulti([g for group in groups for g in group], holdColor=True), "./outputUnion2.dot")
