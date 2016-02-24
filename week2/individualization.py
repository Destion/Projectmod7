from week1.colorRefinement import *


def individualize(g: graph, h: graph):
    a = refineColorsv2(g)
    b = refineColorsv2(h)
    nc = 0
    for v in g.V() and h.V():
        nc = max(v.colornum + 1, nc)
    for v in a:
        if a[v] >= 2:
            # looking for same color as x in aAccent
            y = 0
            u = None
            for u in b:
                y = b[u]
                if a[v] == y:
                    break
            checkforiso(h, b, y, u)
            pass


def checkforiso(h: graph, b: dict, y, u):
    b[u] = y

    pass
