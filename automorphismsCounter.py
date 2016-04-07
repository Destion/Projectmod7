from graphIO import writeDOT
from graphUtil import generateNeighbourList
from gSnellerPartitioning import generatePartitions


def pickFromSet(s):
    e = s.pop()
    s.add(e)
    return e

fileNum = 0

def factorial(x):
    result = 1
    if x < 1:
        raise ValueError
    for i in range(x, 0, -1):
        result *= i
    return result


def drawProgress(G, v, color, done, queue=None):
    global fileNum
    for vv in G.V():
        vv.colornum = -1
    for dv in done:
        dv.colornum = 1
    if queue:
        for c in queue:
            if type(c) == tuple:
                vertex, p = c
                vertex.colornum = 4
            else:
                for cv in c:
                    cv.colornum = 4
    for cv in color:
        cv.colornum = 2
    if v:
        v.colornum = 3
    writeDOT(G, "progress%i.dot" % fileNum)
    fileNum += 1


def countTreeAutomorphismsLS(G, visualize=False):
    p = generatePartitions(G)
    n = generateNeighbourList(G)
    degrees = dict()

    for v in G.V():
        degree = len(n[v])
        degreeSet = degrees.get(degree, 0)
        if degreeSet:
            degreeSet.add(v)
        else:
            degrees[degree] = {v}

    colorOf = dict()
    for color in p:
        for v in color:
            colorOf[v] = color

    queue = []
    done = set()

    for color in p:
        if len(color) > 1 and color <= degrees[1]:
            queue.append(color)
            done = done | color

    automorphisms = 1

    while queue: # is not empty
        newQueue = []
        for color in queue:
            v = pickFromSet(color)
            if visualize:
                drawProgress(G, v, color, done, queue)
            parent = None
            for neighbour in n[v]:
                if len(n[neighbour] & color) > 1 :
                    parent = neighbour
                    break

            if parent is None:
                unvisitedNeighbours = n[v] - done
                if len(unvisitedNeighbours) == 1:
                    parent = unvisitedNeighbours.pop()
                elif len(unvisitedNeighbours) > 1:
                    newQueue.append(color)
                    continue

            if parent:
                if len(colorOf[parent]) > 1 and parent not in done:
                    newQueue.append(colorOf[parent])
                automorphisms *= factorial(len(n[parent] & color))**(len(colorOf[parent]))
                done |= color
            else:
                if len(color) == 2 and len(color&n[v]) == 1:
                    automorphisms *= 2
        queue = newQueue
        for c in queue:
            done |= c

    if visualize:
        drawProgress(G, None, set(), done, queue)
    return automorphisms


def countTreeAutomorphismsRS(G, visualize=False):
    p = generatePartitions(G)
    n = generateNeighbourList(G)
    degrees = dict()

    for v in G.V():
        degree = len(n[v])
        degreeSet = degrees.get(degree, 0)
        if degreeSet:
            degreeSet.add(v)
        else:
            degrees[degree] = {v}

    colorOf = dict()
    for color in p:
        for v in color:
            colorOf[v] = color

    queue = []
    done = set()
    automorphisms = 1
    for c in p:
        if len(c) == 1:
            queue.append((pickFromSet(c), None))
            break
    if not queue:
        for c in p:
            if len(c) == 2:
                r, l = c

                if True or l in n[r]:
                    queue.append((r, None))
                    break
    while queue:
        vertex, parent = queue[-1]
        color = colorOf[vertex]
        del queue[-1]
        for v in n[vertex] - done:
            if v not in done:
                queue.append((v, vertex))
                done |= colorOf[v]
        if parent:
            automorphisms *= factorial(len(n[parent] & color))**(len(colorOf[parent]))
        else:
            automorphisms *= factorial(len(color))
        if visualize:
            drawProgress(G, vertex, color, done, queue)
        done |= color
    if visualize:
        drawProgress(G, None, set(), done, queue)
    return automorphisms












