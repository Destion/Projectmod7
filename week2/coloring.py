from week1.colorRefinement import refineColorsv2
from utilities.graphUtil import disjointUnionMulti


class ColoringCombination(object):
    """
    This class contains the colorings of 2 graphs and makes it easier to check for certain properties.
    A ColoringCombination will automatically define .equal and .bijection, the first is True if
    coloring 1 and 2 contain the same colors in the same amount. The second is True if each color only exists
    once in both colorings.
    """

    def __init__(self, coloringG1: dict, coloringG2: dict, refined=False):
        self.generateCoreValues(coloringG1, coloringG2, refined)

    def generateCoreValues(self, coloringG1: dict, coloringG2: dict, refined):
        """
        Generates all the essential values like .equal and .bijection. Call this when the colorings have changed.
        It is called on __init__ and after the colors have been refined.
        """
        bijection = True
        equal = True
        g1Vertices = set(coloringG1.keys())
        g2Vertices = set(coloringG2.keys())
        g1C = dict()
        g2C = dict()

        multiColors = set()

        maxColor = 0
        for v in g1Vertices:
            color = coloringG1[v]
            g1C[color] = g1C.get(color, 0) + 1
            if color > maxColor:
                maxColor = color
            if g1C[color] == 2:
                bijection = False
                multiColors.add(color)

        for v in g2Vertices:
            color = coloringG2[v]
            g2C[color] = g2C.get(color, 0) + 1
            if color > maxColor:
                maxColor = color
            if g2C[color] == 2:
                bijection = False
        if g1C != g2C:
            equal = False
            bijection = False
        # PyCharm hou je mond, deze variablen worden wel in de constructor toegewezen omdat deze fucntie daar wordt aangeroepen
        self.bijection = bijection
        self.equal = equal
        self.multiColors = multiColors
        self.g1C = g1C
        self.g2C = g2C
        self.g1Vertices = g1Vertices
        self.g2Vertices = g2Vertices
        self.coloringG1 = coloringG1
        self.coloringG2 = coloringG2
        self.maxColor = maxColor
        self.refined = refined

    def buildNewColoringCombinations(self, color=-1):
        """
        Generates a list of new ColoringCombination objects.
        The colorings have been changed in such a way that the first vertex of the given color in coloring 1
        is mapped on every vertex in coloring 2 that has the same color. Every object in the list maps vertex 1 to a
        different in  vertex in coloring 2
        :param color: The color to test for. If left on -1 the object will pick a color from its set of colors that are
            not unique in both graphs
        :return: A list of new colorings that have NOT been refined yet
        """
        if color == -1:
            color = self.multiColors.pop()
            self.multiColors.add(color)
        if color not in self.multiColors:
            return []
        else:
            g1ChosenV = None
            g2WithCol = set()
            for v in self.g1Vertices:
                if color == self.coloringG1[v]:
                    g1ChosenV = v
                    break

            for v in self.g2Vertices:
                if color == self.coloringG2[v]:
                    g2WithCol.add(v)

            newColorings = []
            for v in g2WithCol:
                newColoringG1 = dict()
                newColoringG1.update(self.coloringG1)
                newColoringG2 = dict()
                newColoringG2.update(self.coloringG2)
                newColoringG1[g1ChosenV] = self.maxColor + 1
                newColoringG2[v] = self.maxColor + 1
                newColorings.append(ColoringCombination(newColoringG1, newColoringG2))
            return newColorings

    def applyToGraphs(self, g1, g2):

        for v in g1.V():
            v.colornum = self.coloringG1[v]

        for v in g2.V():
            v.colornum = self.coloringG2[v]

    def refineColors(self, g1, g2):
        """
        Refines the colors with the graphs
        :param g1: graph1
        :param g2: graph2
        :return: Nothing, this function acts on the current object
        """
        if self.refined:
            print("Warning! Refining a ColorCombination that is already flagged as refined!")
        self.applyToGraphs(g1, g2)
        g = disjointUnionMulti([g1, g2], True)
        newColoring = refineColorsv2(g, True)
        newColoringG1 = dict()
        gV = g.V()
        g1V = g1.V()
        for i in range(len(g1V)):
            newColoringG1[g1V[i]] = newColoring[gV[i]]

        newColoringG2 = dict()
        g2V = g2.V()
        for i in range(len(g2V)):
            newColoringG2[g2V[i]] = newColoring[gV[i + len(g1V)]]

        self.generateCoreValues(newColoringG1, newColoringG2, True)

    def __repr__(self):
        return "<CCobject, bijection: %s, equal: %s, refined: %s >"%(self.bijection, self.equal, self.refined)