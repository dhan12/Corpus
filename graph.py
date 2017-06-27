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
            try:
                graphNodes[e['a']].neighbors.append(e['b'])
            except KeyError as e:
                raise Exception('Failed to find node for edge. Error: %s' %
                                (e, ))

        self.nodes = graphNodes
