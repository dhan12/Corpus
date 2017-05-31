#!/usr/bin/python

import json
import sys

class GraphNode():
    def __init__(self, nodeId):
        self.id = nodeId
        self.neighbors = []

class Graph():
    def __init__(self, nodes, edges):
        ''' Construct a graph from nodes and edges
        
        @args nodes dictionary of nodes
        @args edges between nodes
        '''
        graphNodes = {}

        for n in nodes:
            graphNodes[n] = GraphNode(n)

        for e in edges:
            graphNodes[e['a']].neighbors.append(e['b'])

        self.nodes = graphNodes

def initBoards():
    with open('./boards.json', 'r') as input:
        boards = json.loads(input.read())
    return boards


def initEdges():
    with open('./edges.json', 'r') as input:
        edges = json.loads(input.read())
    return edges

def initNodes():
    nodeMap = {}
    with open('./nodes.json', 'r') as input:
        nodes = json.loads(input.read())
        for n in nodes:
            nodeMap[n['id']] = n
    return nodes, nodeMap


def printBoards(boards):
    numBoards = len(boards)
    for i in range(numBoards):
        print 'Board title: ' + boards[i]['title']
        print 'Board members:\n  ' + '\n  '. \
                join([nodeMap[n]['title'] for n in boards[i]['members']])


def printEdges(boards, nodes, nodeMap, edges):
    numBoards = len(boards)
    for i in range(numBoards):
        print 'For board "%s":' % boards[i]['title']

        # Print board relationships
        seenNodes = set()
        for n in nodes:

            if n['id'] not in boards[i]['members']:
                continue

            for e in edges:
                if e['a'] in seenNodes or e['b'] in seenNodes:
                    continue

                if (e['relationship'] == 'directional' and e['a'] == n['id']):
                    print '  %s -- %s --> %s' % \
                        (n['title'], e['description'], nodeMap[e['b']]['title'])
                elif (e['relationship'] == 'directional' and e['b'] == n['id']):
                    print '  %s -- %s --> %s' % \
                        (nodeMap[e['a']]['title'], e['description'], n['title'])
                elif (e['a'] == n['id'] or e['b'] == n['id']):
                    print '  %s -- %s --  %s' % \
                        (n['title'], e['description'], nodeMap[e['b']]['title'])
            seenNodes.add(n['id'])

def printNodes(boards, nodes):
    numBoards = len(boards)
    for i in range(numBoards):
        print 'For board "%s":' % boards[i]['title']
        for n in nodes:
            if n['id'] in boards[i]['members']:
                print '  %s (%s) - %s ...' % \
                      (n['title'], n['id'], n['data'][:25])


def printGraph(g):
    for n in g.nodes:
        print '%s --' % (n,)
        for neighbor in g.nodes[n].neighbors:
            print '  - %s' % (neighbor,)


def printOptions():
    print 'Choose option:'
    print "1 or 'b' to show boards"
    print "2 or 'e' to show edges"
    print "3 or 'n' to show nodes"
    print "4 or 'g' to show graph"
    print "5 or 'q' to quit"

if __name__ == '__main__':
    boards = initBoards()
    edges = initEdges()
    nodes, nodeMap = initNodes()

    g = Graph(nodeMap, edges)
    while True:
        printOptions()
        line = sys.stdin.readline()[:-1]
        if line == '1' or line == 'b':
            printBoards(boards)
        if line == '2' or line == 'e':
            printEdges(boards, nodes, nodeMap, edges)
        if line == '3' or line == 'n':
            printNodes(boards, nodes)
        if line == '4' or line == 'g':
            printGraph(g)
        if line == '5' or line == 'q':
            break
            


