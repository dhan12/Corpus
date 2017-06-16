class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x).rjust(3) + ' ' + str(self.y).rjust(3)

    def __repr__(self):
        return 'Position(%d, %d)' % (self.x, self.y)


def distance(a, b):
    ''' Return an approximate distance. No diagonal moves. '''
    return abs(a.x - b.x) + abs(a.y - b.y)
