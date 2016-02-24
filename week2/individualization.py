from week1.colorRefinement import *


def individualize(G: graph, H: graph):
    maxC = 0
    for v in G.V():
        maxC = max(v.colornum, maxC)
