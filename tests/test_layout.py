import unittest
import graph
import layout
import position


class TestGetLogicGetMoves(unittest.TestCase):
    def setUp(self):
        pass

    def test_one_item(self):
        n = {'a': {}}  # nodes
        e = []  # nodes
        g = graph.Graph(n, e)

        l = layout.Layout()
        l.add('a', g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['a'])
