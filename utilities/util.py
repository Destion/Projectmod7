"""
This file contains general utilities
"""


def compareListsUnordered(l1, l2):
    valueCounts = dict()
    for e in l1 + l2:
        valueCounts[e] = valueCounts.get(e, 0) + 1
    for e in valueCounts:
        if valueCounts[e] % 2 != 0:
            return False
    return True



