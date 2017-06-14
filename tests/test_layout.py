import unittest
import graph
import layout
import position


class TestGetLogicGetMoves(unittest.TestCase):
    def setUp(self):
        pass

    def test_one_item(self):
        n = {'a': {}}  # nodes
        e = []  # edges
        g = graph.Graph(n, e)

        l = layout.Layout()
        l.add('a', g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['a'])

    def test_two_items(self):
        n = {'a': {}, 'b': {}}  # nodes
        e = [{'a': 'a', 'b': 'b'}]  # edges
        g = graph.Graph(n, e)

        l = layout.Layout()
        l.add('a', g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['a'])

        # This depends on layout.DIST_TO_BORDER and DIST_BETWEEN_NODES
        self.assertEquals(position.Position(7, 0), l.nodeToPositionMap['b'])
