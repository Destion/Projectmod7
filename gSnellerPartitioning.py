from graphUtil import generateNeighbourList


def generatePfromColors(G):
    p = []
    colors = dict()
    for v in G.V():
        if v.colornum in colors.keys():
            colors[v.colornum].add(v)
        else:
            colors[v.colornum] = {v}
    keys = list(colors.keys())
    for key in keys:
        p.append(colors[key])
    return p


def generatePartitions(G, usecolors=False):
    neighbours = generateNeighbourList(G)
    p = []
    pSplit = []
    degrees = dict()
    for v in G.V():
        degree = len(neighbours[v])
        if degrees.get(degree, -1) == -1:
            degrees[degree] = {v}
        else:
            degrees[degree].add(v)

    if usecolors:
        p = generatePfromColors(G)
        pSplit = generatePfromColors(G)
    else:
        for k in degrees:
            p.append(degrees[k])
            pSplit.append(degrees[k])

    w = set(range(len(p)))
    while w:
        #print("w: ", w)
        #print("wl: ", [(c, len(p[c])) for c in w])
        aN = w.pop()
        a = p[aN]
        nbs = set()
        for va in a:
            nbs |= neighbours[va]
        # print("nbs: ", nbs)
        for color in pSplit:
            x = nbs & color
            # print("nbs & color: ", x)
            if x:
                for yN in range(len(p)):
                    if len(p[yN]) > 1:
                        y = p[yN]
                        both = x & y
                        ynotx = y - x
                        if both and ynotx:
                            p[yN] = both
                            p.append(ynotx)
                            if yN in w:
                                w.add(len(p) - 1)
                            else:
                                if len(both) <= len(ynotx):
                                    w.add(yN)
                                else:
                                    w.add(len(p) - 1)
    return p


def writeColors(partitions):
    for i in range(len(partitions)):
        for v in partitions[i]:
            v.colornum = i

