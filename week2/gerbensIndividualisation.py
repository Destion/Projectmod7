from basicgraphs import graph


def refineFurther(groups, G: graph):
    newGroups = []
    for group in groups:
        newGroups += refineGroup(group)

def refineGroup(group):
    pass