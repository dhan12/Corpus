import collections
from position import Position
import position

NODE_WIDTH = 11
NODE_HEIGHT = 4
DIST_BETWEEN_NODES = 5


def layoutNodeSort(a, b):
    ''' Sort layout nodes. '''
    if a['fixedPosition'] is None and b['fixedPosition'] is not None:
        return 1
    elif a['fixedPosition'] is not None and b['fixedPosition'] is None:
        return -1

    return b['numNeighbors'] - a['numNeighbors']


class Layout:
    '''
    A layout is composed of nodes and edges.

    The nodes are positioned at a given x,y position. From that position,
        the node will reserve an area of NODE_WIDTH x NODE_HEIGHT.

    The positionMap gives the position of one or more nodes.
    Layout will fix the nodes to those positions.

    Edges define paths between associated nodes.
    '''

    def __init__(self, nodes, positionMap={}):
        # "public"
        self.positionToNodeMap = {}
        self.nodeToPositionMap = {}
        self.edgePath = []
        self.max_x = 0
        self.max_y = 0

        # "private"
        self._min_x = 0
        self._min_y = 0

        self._occupiedNodePoints = set()
        self._occupiedEdgePoints = set()

        # Get order of nodes to place into the layout
        orderedNodes = []
        for n in nodes:
            orderedNodes.append({
                'id': n,
                'fixedPosition': positionMap[n]
                if (n in positionMap)
                else None,
                'numNeighbors': len(nodes[n].neighbors)
            })
        self._orderedNodes = sorted(orderedNodes, cmp=layoutNodeSort)

        # Construct the layout (add nodes and edges)
        self._nodes = nodes
        self._addNodes()
        self._addEdges()
        self._normalize()

    def _normalize(self):
        ''' Shift nodes to all non-negative values '''
        positionToNodeMap = {}
        nodeToPositionMap = {}

        # shift nodes
        for n in self.nodeToPositionMap:
            newp = Position(self.nodeToPositionMap[n].x - self._min_x,
                            self.nodeToPositionMap[n].y - self._min_y)
            positionToNodeMap[newp] = n
            nodeToPositionMap[n] = newp

        # shift edge paths
        for e in self.edgePath:
            path = e['path']
            for p in path:
                p.x -= self._min_x
                p.y -= self._min_y

        self.max_x = self.max_x - self._min_x
        self.max_y = self.max_y - self._min_y
        self._min_x = 0
        self._min_y = 0

        self.positionToNodeMap = positionToNodeMap
        self.nodeToPositionMap = nodeToPositionMap

    def _updateBounds(self, p):
        minx = p.x
        maxx = p.x + NODE_WIDTH
        miny = p.y
        maxy = p.y + NODE_HEIGHT

        if maxx > self.max_x:
            self.max_x = maxx
        if minx < self._min_x:
            self._min_x = minx
        if miny < self._min_y:
            self._min_y = miny
        if maxy > self.max_y:
            self.max_y = maxy

    #
    # Add node functions
    #
    def _hasNode(self, nodeId):
        return nodeId in self.nodeToPositionMap

    def _addNodes(self):
        # Maintain a FIFO queue of nodes to add.
        # Use this queue to a depth first search, ie. add a node,
        #   then all its immediate neighbors,
        #   then neighbors of those neighbors ...
        self._addqueue = collections.deque()

        for n in self._orderedNodes:
            self._addqueue.append({
                'nodeId': n['id'],
                'originPosition': n['fixedPosition']})
            self._addNextNode()

    def _addNextNode(self):
        while True:
            try:
                item = self._addqueue.popleft()
                nodeId = item['nodeId']
                if self._hasNode(nodeId):
                    continue

                nodeId = item['nodeId']
                if 'originPosition' in item:
                    self._putNode(nodeId, item['originPosition'])
                else:
                    self._putNode(nodeId)

                for neighborId in self._nodes[nodeId].neighbors:
                    self._addqueue.append({
                        'nodeId': neighborId,
                        'originPosition': self.nodeToPositionMap[nodeId]
                    })

            except IndexError:
                break

    def _putNode(self, nodeId, startingPosition=None):
        if self._hasNode(nodeId):
            return

        # Find the position
        p = self._choosePosition(startingPosition)

        # Store position
        self.positionToNodeMap[p] = nodeId
        self.nodeToPositionMap[nodeId] = p
        self._occupiedNodePoints.add(p)

        # Mark used positions
        for xi in xrange(NODE_WIDTH):
            for yi in xrange(NODE_HEIGHT):
                self._occupiedNodePoints.add(Position(p.x + xi, p.y + yi))

    def _choosePosition(self, startingPosition=None):
        if startingPosition is None:
            startingPosition = Position(0, 0)

        found = False
        if startingPosition not in self.positionToNodeMap:
            p = startingPosition
            found = True
        else:
            # increase distance until a point is found
            for dist in xrange(10):
                neighPositions = self._getNearestNeighbor(startingPosition,
                                                          dist)

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

            if (self.max_x - self._min_x) > (self.max_y - self._min_y):
                return [Position(start.x, start.y + height),
                        Position(start.x, start.y - height),
                        Position(start.x + width, start.y),
                        Position(start.x - width, start.y)]
            else:
                return [Position(start.x + width, start.y),
                        Position(start.x - width, start.y),
                        Position(start.x, start.y + height),
                        Position(start.x, start.y - height)]

    #
    # Add edge functions
    #
    def _addEdges(self):
        for n in self._nodes:
            for neighborId in self._nodes[n].neighbors:
                self._addEdge(n, neighborId)

    def _addEdge(self, originId, neighborId):
        # Add edge path between the nodes
        startPos, endPos = self._getEdgeEnds(
            self.nodeToPositionMap[originId],
            self.nodeToPositionMap[neighborId])
        path = self._getPathBetweenPoints(startPos, endPos)
        self.edgePath.append(
            {'from': originId, 'to': neighborId, 'path': path})

        # Update bounds
        for p in path:
            self._occupiedEdgePoints.add(p)
            self._updateBounds(p)

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
        poss = filter(
            lambda x:
            x not in self._occupiedNodePoints and
            x not in self._occupiedEdgePoints,
            poss)
        if len(poss) == 0:
            # TODO: find a better value for this,
            #       we are just re-using this point for now
            poss = [Position(pos.x - 1, pos.y + (NODE_HEIGHT / 2))]
        return poss

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
