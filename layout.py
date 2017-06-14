from position import Position

NODE_WIDTH = 11
NODE_HEIGHT = 3
DIST_BETWEEN_NODES = 3


class Layout:
    def __init__(self):

        self.positionToNodeMap = {}
        self.nodeToPositionMap = {}

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self._width = 0
        self._length = 0

    def add(self, nodeId, nodes):
        if self._hasNode(nodeId):
            return

        p = self._choosePosition()
        self.positionToNodeMap[p] = nodeId
        self.nodeToPositionMap[nodeId] = p

        for neighborId in nodes[nodeId].neighbors:
            self._addNeighbor(nodeId, neighborId, nodes)

    def _addNeighbor(self, originId, neighborId, nodes):
        if self._hasNode(neighborId):
            return

        p = self._choosePosition()
        self.positionToNodeMap[p] = neighborId
        self.nodeToPositionMap[neighborId] = p

        for n2 in nodes[neighborId].neighbors:
            self._addNeighbor(neighborId, n2, nodes)

    def _hasNode(self, nodeId):
        return nodeId in self.nodeToPositionMap

    def _getAllShifts(self, distance):
        if distance == 0:
            return [Position(0, 0)]
        if distance == 1:
            width = (2 * int(NODE_WIDTH / 2)) + DIST_BETWEEN_NODES + 1
            height = (2 * int(NODE_HEIGHT / 2)) + DIST_BETWEEN_NODES + 1
            return [Position(width, 0),
                    Position(0, -1 * height),
                    Position(-1 * width, 0),
                    Position(0, height),
                    Position(width, -1 * height),
                    Position(-1 * width, -1 * height),
                    Position(-1 * width, height),
                    Position(width, height)]

    def _choosePosition(self, startingPosition=None):
        if startingPosition is None:
            startingPosition = Position(0, 0)

        if startingPosition not in self.positionToNodeMap:
            self._updateBounds(startingPosition)
            return startingPosition

        # TODO: increase distance until a point is found
        distance = 1
        shifts = self._getAllShifts(distance)

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
        minx = p.x - 1
        maxx = p.x + NODE_WIDTH
        miny = p.y - 1
        maxy = p.y + NODE_HEIGHT

        if maxx > self.max_x:
            self.max_x = maxx
        if minx < self.min_x:
            self.min_x = minx
        if miny < self.min_y:
            self.min_y = miny
        if maxy > self.max_y:
            self.max_y = maxy

        self._width = self.max_x - self.min_x
        self._length = self.max_y - self.min_y
