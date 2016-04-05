from utilities.basicgraphs import *
from utilities.graphIO import loadgraph, writeDOT
from utilities.pythonex1 import createCycleGraph
from week1.colorRefinement import getAllIsomorphisms
from week2.coloring import *


def buildColoringCombinationFromGraphs(g1: graph, g2: graph):
    """
    This script needs a coloring from week1 to work!!!
    :param g1: graph1, with defined colornums
    :param g2: graph2, with defined colornums
    :return: ColoringCombination with of the 2 graphs
    """
    a1 = dict()
    a2 = dict()
    for v in g1.V():
        a1[v] = v.colornum

    for v in g2.V():
        a2[v] = v.colornum
    return ColoringCombination(a1, a2, True)


def areIsomorph(g1: graph, g2: graph):
    stack = [buildColoringCombinationFromGraphs(g1, g2)]
    oldColoring = buildColoringCombinationFromGraphs(g1, g2)
    automorphisms = 0
    while len(stack) != 0:
        cc = stack[-1]
        stack = stack[:-1]

        if cc.bijection:
            # gevonden :D
            automorphisms += 1
        elif cc.equal:
            # Wel equal, maar geen bijection. Dubbele kleuren dus. Tijd om verder te zoeken
            newCCs = cc.buildNewColoringCombinations()
            for newCC in newCCs:
                newCC.refineColors(g1, g2)
                # reset the colors
                oldColoring.applyToGraphs(g1, g2)
            stack += newCCs
        else:
            # tja, als ze niet equal zijn hoeft er eigenlijk niet heel veel te gebreuren
            pass
    # als ze ooit wel isomorf waren , dan waren we nooit hier uitgekomen
    return automorphisms


def refineFurther(groups):
    newGroups = []
    for group in groups:
        for g in group:
            placed = False
            for newGroup in newGroups:
                if newGroup[0] in group and areIsomorph(g, newGroup[0]):
                    print(areIsomorph(g, newGroup[0]))
                    newGroup.append(g)
                    placed = True
                    break
            if not placed:
                newGroups.append([g])
    return newGroups


def getIsomorphismGroups(graphList):
    """
    The full algorithm that converts a list of graphs to a list of groups of isomorphic graphs
    The outcome contains all elements of the input, in isomorphic groups. Every graph in a group is isomorphic with
    every other graph in the groups.
    :param graphList: A list of graphs
    :return: A list containing smaller list. The smaller lists are groups of isomorphic graphs.
    """
    groups, G = getAllIsomorphisms(graphList)
    return refineFurther(groups)

if __name__ == "__main__":
    gl = loadgraph("./../data/torus24.grl", readlist=True)
    # gl = [[disjointUnionMulti([createCycleGraph(1), createCycleGraph(1)]), createCycleGraph(2), createCycleGraph(2)]]
    i = 0
    groups, G = getAllIsomorphisms(gl[0])
    print([len(group) for group in groups])
    groups = refineFurther(groups)
    print([[gl[0].index(g) for g in group] for group in groups])
    writeDOT(disjointUnionMulti([g for group in groups for g in group], holdColor=True), "./outputUnion2.dot")