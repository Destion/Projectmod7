from graphIO import loadgraph, writeDOT


def coloring(G):

	verts = set()

	for vertex in G.V():
		vertex.oldcolor = len(vertex.nbs())
		vertex.newcolor = len(vertex.nbs())
		verts.add(vertex)

	print(verts)
	colordict = dict()

	for v in verts:
		if len(colordict) > 0:
			for key in colordict.keys():
				if key == v.oldcolor:
					if len(colordict[key]) > 0:
						colordict[key].add(v)
						print("append")
					else:
						colordict[key] = set().add(v)
						break
			colordict[v.oldcolor] = set().add(v)
		else:
			colordict[v.oldcolor] = set().add(v)
	print(colordict)


	for vertexi in G.V():
		print("Meer dingen")
		vertexi.colornum = vertexi.oldcolor
	writeDOT(G, "Test.dot")


def neighbourcolor(x, y):
	if len(x.nbs()) != len(y.nbs()):
		return False
	temp1 = set()
	temp2 = set()
	for vx in x.nbs():
		temp1.add(vx.oldcolor)
	for vy in y.nbs():
		temp2.add(vy.oldcolor)
	print(temp1==temp2)
	return temp1 == temp2


G = loadgraph("colorref_smallexample_4_7.grl")

coloring(G)