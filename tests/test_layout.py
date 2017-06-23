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

        l = layout.Layout(g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['n1'])

    def test_two_items(self):
        n = {'n1': {}, 'n2': {}}  # nodes
        e = []  # edges
        g = graph.Graph(n, e)

        l = layout.Layout(g.nodes)
        self.assertEquals(position.Position(0, 0), l.nodeToPositionMap['n1'])

        # This depends on parameters in layout (NODE_WIDTH, NODE_HEIGHT, ...)
        self.assertEquals(position.Position(16, 0), l.nodeToPositionMap['n2'])

    def test_horizontal_edge(self):
        n = {'n1': {}, 'n2': {}}  # nodes
        e = [{'a': 'n1', 'b': 'n2'}]  # edges
        g = graph.Graph(n, e)

        l = layout.Layout(g.nodes)

        # Check the path
        self.assertEquals(5, len(l.edgePath[0]['path']))
        self.assertEquals(position.Position(11, 2), l.edgePath[0]['path'][0])
        self.assertEquals(position.Position(12, 2), l.edgePath[0]['path'][1])
        self.assertEquals(position.Position(13, 2), l.edgePath[0]['path'][2])
        self.assertEquals(position.Position(14, 2), l.edgePath[0]['path'][3])
        self.assertEquals(position.Position(15, 2), l.edgePath[0]['path'][4])

    def test_vertical_edge(self):
        n = {'n1': {}, 'n2': {}, 'n3': {}}  # nodes
        e = [{'a': 'n1', 'b': 'n2'},
             {'a': 'n1', 'b': 'n3'}]  # edges
        g = graph.Graph(n, e)

        l = layout.Layout(g.nodes)

        # n3 should be under n1
        self.assertEquals(position.Position(0, 0),
                          l.nodeToPositionMap['n1'])
        self.assertEquals(
            position.Position(
                0, layout.NODE_HEIGHT + layout.DIST_BETWEEN_NODES),
            l.nodeToPositionMap['n3'])

        # Check the path
        self.assertEquals(5, len(l.edgePath[1]['path']))
        self.assertEquals(position.Position(5, 4), l.edgePath[1]['path'][0])
        self.assertEquals(position.Position(5, 5), l.edgePath[1]['path'][1])
        self.assertEquals(position.Position(5, 6), l.edgePath[1]['path'][2])
        self.assertEquals(position.Position(5, 7), l.edgePath[1]['path'][3])
        self.assertEquals(position.Position(5, 8), l.edgePath[1]['path'][4])

    def test_turn_edge(self):
        n = {'n1': {}, 'n2': {}, 'n3': {}}  # nodes
        e = [{'a': 'n1', 'b': 'n2'},
             {'a': 'n2', 'b': 'n3'}]  # edges
        g = graph.Graph(n, e)

        l = layout.Layout(g.nodes)

        # n2 and n3 are diagonal from each other
        self.assertEquals(
                position.Position(
                    layout.NODE_WIDTH + layout.DIST_BETWEEN_NODES, 0),
                l.nodeToPositionMap['n2'])
        self.assertEquals(
                position.Position(
                    0, layout.NODE_HEIGHT + layout.DIST_BETWEEN_NODES),
                l.nodeToPositionMap['n3'])

        # TODO : improve path validation.
        # Should improve by manually selecting positions in grid
