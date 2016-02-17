from graphIO import loadgraph, writeDOT


def coloring(G):
	for vertex in G.V():
		vertex.oldcolor = -1
		vertex.newcolor = -1

	i = 0
	while colorchanged(G.V()):
		i += 1
		for v in G.V():
			v.oldcolor = v.newcolor
			v.newcolor = -1
			for u in G.V():
				if neighbourcolor(v, u) and u.oldcolor == v.oldcolor:
					u.newcolor = i
					v.newcolor = i

	for vertexi in G.V():
		vertexi.colornum = vertexi.oldcolor
	writeDOT(G, "Test.dot")

def colorchanged(G):
	for v in G:
		if v.oldcolor != v.newcolor:
			return True
	return False


def neighbourcolor(x, y):
	if len(x.nbs()) != len(y.nbs()):
		return False
	temp1 = set()
	temp2 = set()
	for v in x.nbs():
		temp1.add(v.color)
	for u in y.nbs():
		temp2.add(u.color)

	return temp1 == temp2


G = loadgraph("colorref_smallexample_4_16.grl")

coloring(G)