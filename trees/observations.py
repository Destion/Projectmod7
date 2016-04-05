import time

from trees.automorphismsCounter import countTreeAutomorphismsLS, countTreeAutomorphismsRS
from utilities.basicgraphs import *
from utilities.graphIO import writeDOT
from utilities.graphUtil import createGraph
from week1.colorRefinement import refineColorsv2
from week3.gSnellerPartitioning import generatePartitions, writeColors

def generateTree(length):
    G = graph(length)
    done = {G.V()[0]}
    c = 0
    for i in range(1, len(G.V())):
        G.addedge(G.V()[i], G.V()[int((10000.0*time.time()+c)%i)])
        c += 1
        done.add(G.V()[i])
    return G

def createSimpleExample():
    return createGraph(11, [(0,4), (1,4), (4,6), (2, 5 ), (3,5), (5,6), (6,7), (7,8), (8,9), (8,10)])

# g = createGraph(22, [(0,2), (1,2), (2,9), (3,5), (4,5), (5,9), (6,8), (7,8), (8,9),
#                     (9, 10), (10, 11), (11, 12), (11, 13), (11,14), (13, 15), (10, 16), (10, 17), (17, 18), (17, 19), (17,20), (20,21)])

#g = createGraph(10, [(0,1), (1,2), (2,3), (3,4), (4,5), (0,6), (0,7), (5,8), (5,9)])
g = generateTree(3000)
# writeDOT(g, "testTree.dot")
# g.V()[2] = None
p = generatePartitions(g)
# refineColorsv2(g)5
print(countTreeAutomorphismsLS(g, True))
print(countTreeAutomorphismsRS(g, True))
writeColors(p)
writeDOT(g, "testTree.dot")