#!/usr/bin/python

import json
import os
import sys
import print_funcs
from graph import Graph
from position import Position


def initData(dataDir):
    boards = []
    edges = []
    nodeMap = {}
    _nodes = []

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
                _nodes = data['nodes']
    for n in _nodes:
        nodeMap[n['id']] = n
    return boards, nodeMap, edges


def loadData(dataSet='sample-data/sports-teams/'):
    boards, nodeMap, edges = initData(dataSet)
    g = Graph(nodeMap, edges)
    return boards, edges, nodeMap, g


if __name__ == '__main__':

    if len(sys.argv) > 1:
        boards, edges, nodeMap, g = loadData(sys.argv[1])
    else:
        boards, edges, nodeMap, g = loadData()

    while True:
        print_funcs.printOptions()
        line = sys.stdin.readline()[:-1]
        if line == 'b':
            print_funcs.printBoards(boards)
        if line == 'e':
            print_funcs.printEdges(boards, nodeMap, edges)
        if line == 'n':
            print_funcs.printNodes(boards, nodeMap)
        if line == 'g':
            print_funcs.printGraph(g)
        if line == 'r':
            boards, edges, nodeMap, g = loadData()
            print 'Data reloaded'
        if line == 'q':
            break
