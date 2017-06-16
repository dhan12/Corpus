import unittest
import position


class TestPositionDistance(unittest.TestCase):
    def setUp(self):
        pass

    def test_no_distance(self):
        a = position.Position(1, 2)
        b = position.Position(1, 2)
        self.assertEquals(0, position.distance(a, b))

    def test_vert_distance(self):
        a = position.Position(1, 2)
        b = position.Position(1, 3)
        self.assertEquals(1, position.distance(a, b))

    def test_horizontal_distance(self):
        a = position.Position(1, 2)
        b = position.Position(2, 2)
        self.assertEquals(1, position.distance(a, b))

    def test_diagonal_distance(self):
        a = position.Position(1, 1)
        b = position.Position(3, 3)
        self.assertEquals(4, position.distance(a, b))

    def test_sorting(self):
        a = position.Position(1, 1)
        b = position.Position(3, 3)
        c = position.Position(5, 5)
        items = [a, b, c]

        z = position.Position(9, 9)
        sortedItems = sorted(items, key=lambda pos: position.distance(pos, z))
        self.assertEquals(c, sortedItems[0])
        self.assertEquals(b, sortedItems[1])
        self.assertEquals(a, sortedItems[2])
