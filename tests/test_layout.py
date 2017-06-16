import unittest
import graph
import layout
import position


class TestGetLogicGetMoves(unittest.TestCase):
    def setUp(self):
        pass

    def test_one_item(self):
        n = {'n1': {}}  # nodes
        e = []  # edges
        g = graph.Graph(n, e)

        l = layout.Layout()
        l.add('n1', g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['n1'])

    def test_two_items(self):
        n = {'n1': {}, 'n2': {}}  # nodes
        e = []  # edges
        g = graph.Graph(n, e)

        l = layout.Layout()
        l.add('n1', g.nodes)
        l.add('n2', g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['n1'])

        # This depends on parameters in layout (NODE_WIDTH, NODE_HEIGHT, ...)
        self.assertEquals(position.Position(16, 0), l.nodeToPositionMap['n2'])

    def test_horizontal_edge(self):
        n = {'n1': {}, 'n2': {}}  # nodes
        e = [{'a': 'n1', 'b': 'n2'}]  # edges
        g = graph.Graph(n, e)

        l = layout.Layout()
        l.add('n1', g.nodes)

        # Check the path
        self.assertEquals(4, len(l.edgePath[0]['path']))
        self.assertEquals(position.Position(11, 1), l.edgePath[0]['path'][0])
        self.assertEquals(position.Position(12, 1), l.edgePath[0]['path'][1])
        self.assertEquals(position.Position(13, 1), l.edgePath[0]['path'][2])
        self.assertEquals(position.Position(14, 1), l.edgePath[0]['path'][3])
