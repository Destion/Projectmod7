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
    while len(stack) != 0:
        cc = stack[-1]
        stack = stack[:-1]

        if cc.bijection:
            # gevonden :D
            return True
        elif cc.equal:
            # Wel equal, maar geen bijection. Dubbele kleuren dus. Tijd om verder te zoeken
            newCCs = cc.buildNewColoringCombinations()
            for newCC in newCCs:
                newCC.refineColors(g1, g2)
                # reset the colors
                oldColoring.applyToGraphs(g1, g2)
            stack += newCCs
        else:
            # tja, als ze niet equal zijn hoeft er eignelijk niet heel veel te gebreuren
            pass
    # als ze ooit wel isomorf waren , dan waren we nooit hier uitgekomen
    return False


def refineFurther(groups):
    newGroups = []
    for group in groups:
        for g in group:
            placed = False
            for newGroup in newGroups:
                if newGroup[0] in group and areIsomorph(g, newGroup[0]):
                    newGroup.append(g)
                    placed = True
                    break
            if not placed:
                newGroups.append([g])
    return newGroups

if __name__ == "__main__":
    gl = loadgraph("./../data/wheelstar12.grl", readlist=True)
    gl = [[disjointUnionMulti([createCycleGraph(3), createCycleGraph(3)]), createCycleGraph(6), createCycleGraph(6)]]
    i = 0
    groups, G = getAllIsomorphisms(gl[0])
    print([len(group) for group in groups])
    groups = refineFurther(groups)
    print([len(group) for group in groups])
    writeDOT(disjointUnionMulti([g for group in groups for g in group], holdColor=True), "./outputUnion2.dot")