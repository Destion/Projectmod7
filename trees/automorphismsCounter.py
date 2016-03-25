import math

from utilities.graphUtil import generateNeighbourList
from week3.gSnellerPartitioning import generatePartitions


def pickFromSet(s):
    e = s.pop()
    s.add(e)
    return e


def countTreeAutomorphisms(G):
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
            parent = None
            for neighbour in n[v]:
                if neighbour not in done and len(n[neighbour] & color) > 1 :
                    parent = neighbour
                    break
            print(parent)

            if parent is None:
                unvisitedNeighbours = n[v] - done
                print (unvisitedNeighbours)
                if len(unvisitedNeighbours) == 1:
                    parent = unvisitedNeighbours.pop()
                elif len(unvisitedNeighbours) > 1:
                    newQueue.append(color)
                    continue


            if parent:
                if len(colorOf[parent]) > 1:
                    newQueue.append(colorOf[parent])
                print("(%i!)**(%i)"%(len(n[parent] & color), len(colorOf[parent])))
                automorphisms *= (math.factorial(len(n[parent] & color)))**(len(colorOf[parent]))
                done |= color
        queue = newQueue
        print ("Queue: ", queue)

    return automorphisms









