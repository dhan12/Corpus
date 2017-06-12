import layout


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
                        (item['title'], item['id'], item['data'][:25].replace('\n',' '))
                seenNodes.add(n)

    orphanedNodes = [n for n in nodeMap if n not in seenNodes]
    if len(orphanedNodes) > 0:
        print 'Items not on a board:'
    for n in orphanedNodes:
        item = nodeMap[n]
        print '  %s (%s) - %s ...' % \
                (item['title'], item['id'], item['data'][:25].replace('\n',' '))


def printGraph(g):
    _layout = layout.Layout()

    for n in g.nodes:
        _layout.add(n, g.nodes)

    for p in _layout.positionToNodeMap:
        print p, _layout.positionToNodeMap[p]

    for n in g.nodes:
        node = g.nodes[n]
        for neighbor in node.neighbors:
            print _layout.nodeToPositionMap[n], _layout.nodeToPositionMap[neighbor]

    '''
    y = layout._min_y
    while y <= layout._max_y:
        items = []
        x = layout._min_x
        while x <= layout._max_x:
            p = Position(x, y)
            try:
                nodeId = layout.positionToNodeMap[p] 
                items.append(nodeId.ljust(20))
            except KeyError:
                items.append(''.ljust(20))
            x = x + 1
        print '  '.join(items)
        y = y + 1
    '''
