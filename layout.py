from random import shuffle
from position import Position


class Layout:
    def __init__(self):

        self.positionToNodeMap = {}
        self.nodeToPositionMap = {}

        self._min_x = 0
        self._max_x = 0
        self._min_y = 0
        self._max_y = 0

        self._width = 0
        self._length = 0

    def add(self, nodeId, nodes):
        if self.hasNode(nodeId):
            return

        p = self._choosePosition()
        self.positionToNodeMap[p] = nodeId
        self.nodeToPositionMap[nodeId] = p

        for neighborId in nodes[nodeId].neighbors:
            self.addNeighbor(nodeId, neighborId, nodes)

    def addNeighbor(self, originId, neighborId, nodes):
        if self.hasNode(neighborId):
            return

        p = self._choosePosition()
        self.positionToNodeMap[p] = neighborId
        self.nodeToPositionMap[neighborId] = p

        for n2 in nodes[neighborId].neighbors:
            self.addNeighbor(neighborId, n2, nodes)

    def hasNode(self, nodeId):
        return nodeId in self.nodeToPositionMap

    def _getAllShifts(self, distance):
        if distance == 0:
            return [Position(0, 0)]
        if distance == 1:
            return [Position(0, -1),
                    Position(0, 1),
                    Position(1, 0),
                    Position(1, 1),
                    Position(1, -1),
                    Position(-1, 0),
                    Position(-1, 1),
                    Position(-1, -1)]

    def _choosePosition(self, startingPosition=None):
        if startingPosition is None:
            startingPosition = Position(0, 0)

        if startingPosition not in self.positionToNodeMap:
            self._updateBounds(startingPosition)
            return startingPosition

        distance = 1
        shifts = self._getAllShifts(distance)
        shuffle(shifts)

        for s in shifts:
            p = Position(startingPosition.x + s.x, startingPosition.y + s.y)
            if p in self.positionToNodeMap:
                continue
            break

        if p is None:
            print 'Board is full'
            raise Exception('Board is full')

        self._updateBounds(p)

        return p

    def _updateBounds(self, p):
        if p.x > self._max_x:
            self._max_x = p.x
        if p.x < self._min_x:
            self._min_x = p.x
        if p.y < self._min_y:
            self._min_y = p.y
        if p.y > self._max_y:
            self._max_y = p.y

        self._width = self._max_x - self._min_x
        self._length = self._max_y - self._min_y
