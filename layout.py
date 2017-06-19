from position import Position
import position

NODE_WIDTH = 11
NODE_HEIGHT = 4
DIST_BETWEEN_NODES = 5


class Layout:
    def __init__(self):

        self.positionToNodeMap = {}
        self.nodeToPositionMap = {}
        self.edgePath = []

        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

        self._width = 0
        self._length = 0
        self._occupiedNodePoints = set()

    def add(self, nodeId, nodes):
        if self._hasNode(nodeId):
            return

        self._putNode(nodeId)

        for neighborId in nodes[nodeId].neighbors:
            self._addNeighbor(nodeId, neighborId, nodes)

    def normalize(self):
        ''' Shift nodes to all non-negative values '''
        positionToNodeMap = {}
        nodeToPositionMap = {}

        # shift nodes
        for n in self.nodeToPositionMap:
            newp = Position(self.nodeToPositionMap[n].x - self.min_x,
                            self.nodeToPositionMap[n].y - self.min_y)
            positionToNodeMap[newp] = n
            nodeToPositionMap[n] = newp

        # shift edge paths
        for e in self.edgePath:
            path = e['path']
            for p in path:
                p.x -= self.min_x
                p.y -= self.min_y

        self.max_x = self.max_x - self.min_x
        self.max_y = self.max_y - self.min_y
        self.min_x = 0
        self.min_y = 0

        self.positionToNodeMap = positionToNodeMap
        self.nodeToPositionMap = nodeToPositionMap

    def _addNeighbor(self, originId, neighborId, nodes):

        # Give node a position
        if not self._hasNode(neighborId):
            self._putNode(neighborId)

        # Add edge path between the nodes
        startPos, endPos = self._getEdgeEnds(
            self.nodeToPositionMap[originId],
            self.nodeToPositionMap[neighborId])
        path = self._getPathBetweenPoints(startPos, endPos)
        self.edgePath.append(
                {'from': originId, 'to': neighborId, 'path': path})

        # Update bounds
        for p in path:
            self._updateBounds(p)

        # Add neighbors of neighbors
        for n2 in nodes[neighborId].neighbors:
            self._addNeighbor(neighborId, n2, nodes)

    def _putNode(self, nodeId):
        if self._hasNode(nodeId):
            return

        # Find the position
        p = self._choosePosition()

        # Store position
        self.positionToNodeMap[p] = nodeId
        self.nodeToPositionMap[nodeId] = p
        self._occupiedNodePoints.add(p)

        # Mark used positions
        for xi in xrange(NODE_WIDTH):
            for yi in xrange(NODE_HEIGHT):
                self._occupiedNodePoints.add(Position(p.x + xi, p.y + yi))

    def _hasNode(self, nodeId):
        return nodeId in self.nodeToPositionMap

    def _getEdgeEnds(self, posA, posB):
        ptsA = self._findMidOfBorders(posA)
        ptsB = self._findMidOfBorders(posB)
        fromA, toB = self._findClosestPair(ptsA, ptsB)
        return fromA, toB

    def _findMidOfBorders(self, pos):
        poss = [Position(pos.x - 1, pos.y + (NODE_HEIGHT / 2)),
                Position(pos.x + NODE_WIDTH, pos.y + (NODE_HEIGHT / 2)),
                Position(pos.x + (NODE_WIDTH / 2), pos.y - 1),
                Position(pos.x + (NODE_WIDTH / 2), pos.y + NODE_HEIGHT)]
        return filter(lambda x: x not in self._occupiedNodePoints, poss)

    def _findClosestPair(self, ptsA, ptsB):
        mindist = None
        for a in ptsA:
            for b in ptsB:
                dist = position.distance(a, b)
                if (mindist is None) or (dist < mindist):
                    mindist = dist
                    bestA = a
                    bestB = b
        if mindist is None:
            raise Exception('Cannot find edge ends')
        return bestA, bestB

    def _getPathBetweenPoints(self, posA, posB):
        path = self._completePath([posA], posB)
        if path:
            if len(path) <= 0:
                raise Exception('Bad path between points', posA, posB)
            return path
        raise Exception('Cannot find path between points', posA, posB)

    def _completePath(self, currentPath, finalPosition):
        lastStep = currentPath[-1]
        if lastStep == finalPosition:
            return currentPath

        maxPts = 1000
        if len(currentPath) > maxPts:
            raise Exception('currentPath > %d points (%s)' %
                            (maxPts, str(currentPath)))

        # Get possible moves
        candidates = [Position(lastStep.x + 1, lastStep.y),
                      Position(lastStep.x - 1, lastStep.y),
                      Position(lastStep.x, lastStep.y + 1),
                      Position(lastStep.x, lastStep.y - 1)]

        # Eliminate bad moves
        candidates = filter(
                lambda x:
                x not in currentPath and x not in self._occupiedNodePoints,
                candidates)

        # Prioritize possible moves
        sortedItems = sorted(
                candidates,
                key=lambda pos: position.distance(pos, finalPosition))

        # Recursively test possible path
        for s in sortedItems:
            currentPath.append(s)
            if self._completePath(currentPath, finalPosition):
                return currentPath
            currentPath.drop()

        return False

    def _getNearestNeighbor(self, start, distance):
        if start is None:
            start = Positon(0, 0)

        width = NODE_WIDTH + DIST_BETWEEN_NODES
        height = NODE_HEIGHT + DIST_BETWEEN_NODES

        if distance == 0:
            return [Position(start.x, start.y)]
        if distance == 1:
            return [Position(start.x + width, start.y),
                    Position(start.x, start.y + height),
                    Position(start.x - width, start.y),
                    Position(start.x, start.y - height)]
        if distance == 2:
            return [Position(start.x + width, start.y - height),
                    Position(start.x - width, start.y - height),
                    Position(start.x - width, start.y + height),
                    Position(start.x + width, start.y + height),
                    Position(start.x + (2 * width), start.y),
                    Position(start.x, start.y + (2 * height)),
                    Position(start.x - (2 * width), start.y),
                    Position(start.x, start.y - (2 * height))]
        if distance > 2:
            width *= distance
            height *= distance
            return [Position(start.x + width, start.y),
                    Position(start.x, start.y + height),
                    Position(start.x - width, start.y),
                    Position(start.x, start.y - height)]

    def _choosePosition(self, startingPosition=None):
        if startingPosition is None:
            startingPosition = Position(0, 0)

        if startingPosition not in self.positionToNodeMap:
            self._updateBounds(startingPosition)
            return startingPosition

        # increase distance until a point is found
        found = False
        for dist in xrange(5):
            neighPositions = self._getNearestNeighbor(startingPosition, dist)

            for p in neighPositions:
                if p in self.positionToNodeMap:
                    continue
                found = True
                break
            if found:
                break

        if not found:
            raise Exception('Cant find position near %s', startingPosition)

        self._updateBounds(p)

        return p

    def _updateBounds(self, p):
        minx = p.x
        maxx = p.x + NODE_WIDTH
        miny = p.y
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
