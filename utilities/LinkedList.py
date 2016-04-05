class DLLItem(object):
    def __init__(self, value, llist, left, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.llist = llist

    def _changeLL_(self, llist, left, right=None):
        self.llist = llist
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.value)


class DLLIterator(object):
    def __init__(self, element):
        self.e = element

    def __next__(self):
        if self.e is None:
            raise StopIteration
        else:
            answer = self.e
            self.e = self.e.right
            return answer.value


class NoLinkException(Exception):
    pass


class DLL(object):
    def __init__(self, itemlink=False):
        self.left = None
        self.right = None
        self.length = 0
        if itemlink:
            self.link = dict()
        else:
            self.link = None

    def __len__(self):
        return self.length

    def __iter__(self):
        return DLLIterator(self.left)

    def add(self, value, addPointer=False):
        item = DLLItem(value, self, self.right)
        if addPointer:
            value.dllItem = item
        if self.length == 0:
            self.left = item
            self.right = item
        else:
            self.right.right = item
            self.right = item
        if self.link is not None:
            self.link[value] = item
        self.length += 1
        return item

    def __repr__(self):
        s = "<DLL, len= %i, elements= "
        for e in self:
            if e.right is not None:
                s += str(e) + " - "
            else:
                s += str(e) + " >"
        return s

    def getLinkedItem(self, value):
        if self.link is None:
            raise NoLinkException("Link disabled")

        if value not in self.link.keys():
            raise NoLinkException("Value not in list")

        return self.link[value]

    def linkRemove(self, value):
        self.remove(self.getLinkedItem(value))

    def remove(self, item: DLLItem):
        if self.left == item:
            self.left = item.right
        if self.right == item:
            self.right = item.left
        if item.right is not None:
            item.right.left = item.left
        if item.left is not None:
            item.left.right = item .right
        self.length -= 1
        item.right = item.left = item.llist = None
        if self.link is not None:
            del self.link[item.value]

if __name__ == "__main__":
    l = DLL(False)
    dllis = dict()
    for i in range(1000000):
        dllis[i] = l.add(i)

    for e in l:
        if e%2 == 1:
            l.remove(dllis[e])
    print(len(l))
    print(5822 in l)
