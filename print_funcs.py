import layout
import position


def fillArray(text, length):

    result = list(text[:length])

    diff = length - len(result)
    if diff > 0:
        for _ in xrange(diff):
            result.append(' ')
    return result


def printOptions():
    print 'Choose option:'
    print "'b' to show boards"
    print "'e' to show edges"
    print "'n' to show nodes"
    print "'g' to show graph"
    print "'r' to reload data"
    print "'q' to quit"


def printBoards(boards):
    numBoards = len(boards)
    for i in range(numBoards):
        print 'Board title: ' + boards[i]['title']
        print 'Board members: ' + ', '. \
            join([nodeMap[n]['title'] for n in boards[i]['members']])


def printEdges(boards, nodeMap, edges):
    print 'Edges:'
    numBoards = len(boards)

    # Print board relationships
    seenNodes = set()
    for n in nodeMap:
        item = nodeMap[n]

        for e in edges:
            if e['a'] in seenNodes or e['b'] in seenNodes:
                continue

            if (e['relationship'] == 'directional' and e['a'] == n):
                print '  %s -- %s --> %s' % \
                    (item['title'], e['description'], nodeMap[e['b']]['title'])
            elif (e['relationship'] == 'directional' and e['b'] == n):
                print '  %s -- %s --> %s' % \
                    (nodeMap[e['a']]['title'], e['description'], item['title'])
            elif (e['a'] == n or e['b'] == n):
                print '  %s -- %s --  %s' % \
                    (item['title'], e['description'], nodeMap[e['b']]['title'])
        seenNodes.add(n)


def printNodes(boards, nodeMap):
    seenNodes = set()

    numBoards = len(boards)
    for i in range(numBoards):
        print 'For board "%s":' % boards[i]['title']
        for n in nodeMap:
            if n in boards[i]['members']:
                item = nodeMap[n]
                print '  %s (%s) - %s ...' % \
                    (item['title'], item['id'],
                     item['data'][:25].replace('\n', ' '))
                seenNodes.add(n)

    orphanedNodes = [n for n in nodeMap if n not in seenNodes]
    if len(orphanedNodes) > 0:
        print 'Items not on a board:'
    for n in orphanedNodes:
        item = nodeMap[n]
        print '  %s (%s) - %s ...' % \
            (item['title'], item['id'], item['data'][:25].replace('\n', ' '))


def printGraph(g):
    _layout = layout.Layout(g.nodes)

    for p in _layout.positionToNodeMap:
        print p, _layout.positionToNodeMap[p]

    for n in g.nodes:
        node = g.nodes[n]
        for neighbor in node.neighbors:
            print _layout.nodeToPositionMap[n], \
                _layout.nodeToPositionMap[neighbor]

    print 'max_x: %d, max_y: %d' % (_layout.max_x, _layout.max_y)

    # set up blank canvas
    lines = []
    for y in xrange(_layout.max_y + 1):
        lines.append([])
        numLines = len(lines)
        for x in xrange(_layout.max_x + 1):
            lines[numLines - 1].append(' ')

    # add node text
    for y in xrange(_layout.max_y):
        for x in xrange(_layout.max_x):
            p = position.Position(x, y)
            try:
                nodeId = _layout.positionToNodeMap[p]
                print nodeId, p, ''.join(lines[y + 1])

                # Add text to put inside the node
                # It just has the node id with a couple blank lines
                lines[y + 1] = lines[y + 1][:x] + ['|'] + \
                    fillArray(nodeId, layout.NODE_WIDTH - 2) + ['|'] + \
                    lines[y][x + layout.NODE_WIDTH:]
                lines[y + 2] = lines[y + 2][:x] + ['|'] + \
                    fillArray('', layout.NODE_WIDTH - 2) + ['|'] + \
                    lines[y + 1][x + layout.NODE_WIDTH:]
                lines[y + 3] = lines[y + 3][:x] + ['|'] + \
                    fillArray('', layout.NODE_WIDTH - 2) + ['|'] + \
                    lines[y + 2][x + layout.NODE_WIDTH:]
                print nodeId, p, ''.join(lines[y + 1])
            except KeyError:
                pass

    # add borders
    borderStr = ['+'] + ['-' for _ in xrange(layout.NODE_WIDTH - 2)] + ['+']
    for y in xrange(_layout.max_y + 1):
        for x in xrange(_layout.max_x + 1):
            p = position.Position(x, y)
            try:
                nodeId = _layout.positionToNodeMap[p]

                # top border
                lines[y] = lines[y][:x] + \
                    borderStr + lines[y][x + layout.NODE_WIDTH:]

                # bottom border
                bottom = y + layout.NODE_HEIGHT - 1
                lines[bottom] = lines[bottom][:x] + \
                    borderStr + lines[bottom][x + layout.NODE_WIDTH:]
            except KeyError:
                pass

    # add edge paths
    pathid = 0
    for e in _layout.edgePath:
        print 'edge from %s to %s' % (e['from'], e['to'])
        path = e['path']
        for p in path:
            lines[p.y][p.x] = str(pathid)
        pathid += 1

    for l in lines:
        print ''.join(l)
