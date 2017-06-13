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
