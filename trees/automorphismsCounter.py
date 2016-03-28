import math

from utilities.graphUtil import generateNeighbourList
from week3.gSnellerPartitioning import generatePartitions


def pickFromSet(s):
    e = s.pop()
    s.add(e)
    return e


def countTreeAutomorphismsLS(G):
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
    ronde = 1
    while queue: # is not empty
        newQueue = []
        for color in queue:

            v = pickFromSet(color)
            v.colornum = ronde
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
                automorphisms *= math.factorial(len(n[parent] & color))**(len(colorOf[parent]))
                done |= color
        queue = newQueue
        for c in queue:
            done |= c
        ronde += 1

    return automorphisms

def countTreeAutomorphismsRS(G):
    p = generatePartitions(G)
    n = generateNeighbourList(G)
    degrees = dict()
    step = 1

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
                if l in n[r]:
                    queue.append((r, None))
                    break
    while queue:
        vertex, parent = queue[-1]
        vertex.label = step
        vertex.colornum = step
        step += 1
        color = colorOf[vertex]
        del queue[-1]
        for v in n[vertex] - done:
            if v not in done:
                queue.append((v, vertex))
                done |= colorOf[v]
        if parent:
            automorphisms *= math.factorial(len(n[parent] & color))**(len(colorOf[parent]))
        else:
            automorphisms *= math.factorial(len(color))
        done |= color
    return automorphisms












