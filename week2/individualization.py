from week1.colorRefinement import *


def individualize(G: graph, H: graph):
    a = refineColorsv2(G)
    aAccent = refineColorsv2(H)
    nc = 0
    for v in G.V() and H.V():
        nc = max(v.colornum + 1, nc)
    for v in a:
        if a[v] >= 2:
            pass
