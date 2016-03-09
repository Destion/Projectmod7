
def generatePartitions(G):
    p = [set(G.V())]
    # TODO: neighbours
    neighbours = dict()
    # TODO: splits p op in degrees
    w = {0}
    while w:
        aN = w.pop()
        a = p[aN]
        x = set()
        # TODO: dat ene met dat splitsen in gerbens boekje
        for va in a:
            x |= neighbours[va]

        for yN in {c for c in range(len(p)) if x&p[c] and p[c]-x}:
            y = p[yN]
            p[yN] = x&y
            p.append(y-x)
            if yN in w:
                w.add(len(p)-1)
            else:
                if len(x&y) <= len(y-x):
                    w.add(yN)
                else:
                    w.add(len(p) - 1)
