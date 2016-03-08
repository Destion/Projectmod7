from utilities.basicgraphs import *


def createLinkedGraph(n, edges):
    g = graph(n)
    for i in range(edges):
        g.addedge(g[i], g[(i + 1)%n])
    return g


def createPathGraph(n):
    return createLinkedGraph(n, n-1)


def createCycleGraph(n):
    return createLinkedGraph(n, n)


def createCompleteGraph(n):
    g = graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            g.addedge(g[i], g[j])
    return g


def disjointUnion(g: graph, h: graph):
    f = graph(len(g.V()) + len(h.V()))
    print(f)
    combinedList = g.V() + h.V()
    for i in range(len(combinedList)):
        v = combinedList[i]
        for e in v.inclist():
            if e.tail() == v:
                f.addedge(f[i], f[combinedList.index(e.head())])

    return f

if __name__ == "__main__":
    print(createPathGraph(10))
    print(createCycleGraph(10))
    print(createCompleteGraph(20))
    print(disjointUnion(createPathGraph(5), createCycleGraph(3)))
