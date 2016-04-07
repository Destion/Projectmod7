from time import time

from utilities.graphIO import writeDOT, loadgraph


def colorref(G):

    for v in G.V():
        v.colornum=1 # Uniform coloring
    for v in G.V():
            v.nbnum=tuple(sorted([i.colornum for i in v.nbs()])) # Determine neighbour coloring
    l=0
    while len(set(v.nbnum for v in G.V()))!=l:  # While partition is refined
        k=0 # First color number
        l=(len(set(v.nbnum for v in G.V())))
        for i in set(v.nbnum for v in G.V()): # Loops along all different sorts of neighbour sets
            for v in G.V():       # Colors numbers with same colored neighbours the same
                if v.nbnum==i:    #
                    v.colornum=k  #
            k+=1                  #
        for v in G.V():
            v.nbnum=tuple(sorted([i.colornum for i in v.nbs()])) # Determine new neighbour coloring
    return G


if __name__ == "__main__":
    begin=time()
    G=loadgraph("./colorref_largeexample_4_1026.grl",readlist=True)
    colorref(G[0][0])
    writeDOT(G[0][0],"bla")
    end=time()
    print(end-begin)

    begin=time()
    G=loadgraph("./colorref_smallexample_4_16.grl",readlist=True)
    colorref(G[0][1])
    writeDOT(G[0][1],"bla")
    end=time()
    print(end-begin)

