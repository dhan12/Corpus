#!/usr/bin/python

import json
import os
import sys
from graph import Graph
from layout import Layout
from position import Position


def initData(dataDir):
    boards = []
    edges = []
    nodes = []
    nodeMap = {}

    for filename in os.listdir(dataDir):
        inputFile = os.path.join(dataDir, filename)
        with open(inputFile, 'r') as input:
            try:
                data = json.loads(input.read())
            except ValueError as e:
                print 'Failed to load' + inputFile
                continue
            if 'boards' in data:
                boards += data['boards']

            if 'edges' in data:
                edges += data['edges']

            if 'nodes' in data:
                nodes = data['nodes']
    for n in nodes:
        nodeMap[n['id']] = n
    return boards, nodeMap, edges


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
    layout = Layout()

    for n in g.nodes:
        layout.add(n, g.nodes)

    for p in layout.positionToNodeMap:
        print p, layout.positionToNodeMap[p]

    for n in g.nodes:
        node = g.nodes[n]
        for neighbor in node.neighbors:
            print layout.nodeToPositionMap[n], layout.nodeToPositionMap[neighbor]

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

def printOptions():
    print 'Choose option:'
    print "'b' to show boards"
    print "'e' to show edges"
    print "'n' to show nodes"
    print "'g' to show graph"
    print "'r' to reload data"
    print "'q' to quit"

def loadData():
    boards, nodeMap, edges = initData('../Corpus-cpp-data/')
    g = Graph(nodeMap, edges)
    return boards, edges, nodeMap, g

if __name__ == '__main__':

    boards, edges, nodeMap, g = loadData()

    while True:
        printOptions()
        line = sys.stdin.readline()[:-1]
        if line == 'b':
            printBoards(boards)
        if line == 'e':
            printEdges(boards, nodeMap, edges)
        if line == 'n':
            printNodes(boards, nodeMap)
        if line == 'g':
            printGraph(g)
        if line == 'r':
            boards, edges, nodeMap, g = loadData()
            print 'Data reloaded'
        if line == 'q':
            break



