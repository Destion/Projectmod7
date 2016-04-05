from utilities.basicgraphs import *
from utilities.graphIO import loadgraph
from utilities.graphUtil import isConnected
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


def areIsomorph(g1: graph, g2: graph, aut):
    stack = [buildColoringCombinationFromGraphs(g1, g2)]
    oldColoring = buildColoringCombinationFromGraphs(g1, g2)
    automorphisms = 0
    while len(stack) != 0:
        cc = stack[-1]
        stack = stack[:-1]

        if cc.bijection:
            # gevonden :D
            if aut:
                automorphisms += 1
            else:
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
            # tja, als ze niet equal zijn hoeft er eigenlijk niet heel veel te gebreuren
            pass
    # als ze ooit wel isomorf waren , dan waren we nooit hier uitgekomen
    return automorphisms


def refineFurther(groups, aut):
    newGroups = []
    automorphisms = dict()
    graphs = len([g for group in groups for g in group ])
    counter = 1
    for group in groups:
        for g in group:
            print()
            print("Checking graph %i/%i"%(counter, graphs))
            counter += 1
            placed = False
            for newGroup in newGroups:
                if newGroup[0] in group:
                    out = areIsomorph(g, newGroup[0], False)
                    if out:
                        newGroup.append(g)
                        placed = True
                        break
            if not placed:
                newGroups.append([g])
                print("New group made...")
                if aut:
                    print("Counting automorphisms...")
                    print("Graph is %sconnected"%("" if isConnected(g) else "not "))
                    automorphisms[g] = areIsomorph(g, disjointUnionMulti([g], True), True)
    return newGroups, automorphisms


def output(gl, isomorphisms, automorphisms):
    str1 = "Sets of isomorphic graphs:\t\t\t"
    print("\n\n")
    if automorphisms:
        print(str1, "Automorphisms:")
    else:
        print(str1)
    for group in isomorphisms:
        if automorphisms:
            print([gl.index(g) for g in group], " " * len(str1), automorphisms[group[0]])
        else:
            print([gl.index(g) for g in group])


def getIsomorphismGroups(graphList, aut=False):
    """
    The full algorithm that converts a list of graphs to a list of groups of isomorphic graphs
    The outcome contains all elements of the input, in isomorphic groups. Every graph in a group is isomorphic with
    every other graph in the groups.
    :param graphList: A list of graphs
    :return: A list containing smaller list. The smaller lists are groups of isomorphic graphs.
    """
    groups, G = getAllIsomorphisms(graphList)
    further, automorphisms = refineFurther(groups, aut)
    output(graphList, further, automorphisms)
    return further

if __name__ == "__main__":
    gl = loadgraph("./../data/products72.grl", readlist=True)
    # gl = [[disjointUnionMulti([createCycleGraph(1), createCycleGraph(1)]), createCycleGraph(2), createCycleGraph(2)]]
    getIsomorphismGroups(gl[0], True)