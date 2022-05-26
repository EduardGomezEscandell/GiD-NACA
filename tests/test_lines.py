import unittest
import numpy as np

from src.gid_tools import lines

class TestAirfoil (unittest.TestCase):

    class _DummyGeometry():
        """Small version of Gid2DGeometry"""
        def __init__(self):
            self.lines = []
            self.points = []

        def new_point(self, coords: np.ndarray) -> int:
            self.points.append(np.array(coords))
            return len(self.points)

        def new_1d_shape(self, type, *args, **kwargs) -> lines.Shape1D:
            return lines.LineFactory(self, type, *args, **kwargs)

    def test_factory(self):
        geometry = self._DummyGeometry()

        line = lines.LineFactory(geometry, "line")
        self.assertTrue(isinstance(line, lines.Line))

        line = lines.LineFactory(geometry, "semicircle")
        self.assertTrue(isinstance(line, lines.Semicircle))

        line = lines.LineFactory(geometry, "sEmiCirCLE")
        self.assertTrue(isinstance(line, lines.Semicircle))

        line = lines.LineFactory(geometry, "polygon")
        self.assertTrue(isinstance(line, lines.Polygon))
        line._Polygon__closed = True  # Hacky trick to prevent warning

    def test_line(self):
        geometry = self._DummyGeometry()

        line = lines.LineFactory(geometry, "line")
        line.new_point([0, 1])
        line.new_point([2, 3])

        self.assertEqual(geometry.points[0][0], 0)
        self.assertEqual(geometry.points[0][1], 1)
        self.assertEqual(geometry.points[1][0], 2)
        self.assertEqual(geometry.points[1][1], 3)

        self.assertEqual(line.gid_command(), "Geometry Create Line join 1 2 nojoin Escape Escape Escape\n")

    def test_semicircle(self):
        geometry = self._DummyGeometry()

        semicircle = lines.LineFactory(geometry, "semicircle")
        semicircle.new_point([-1, 0])
        semicircle.new_point([0, 1])
        semicircle.new_point([1, 0])

        self.assertEqual(geometry.points[0][0], -1)
        self.assertEqual(geometry.points[0][1], 0)

        self.assertEqual(geometry.points[1][0], 0)
        self.assertEqual(geometry.points[1][1], 1)

        self.assertEqual(geometry.points[2][0], 1)
        self.assertEqual(geometry.points[2][1], 0)

        self.assertEqual(semicircle.gid_command(), "Geometry Create Arc join 1 2 3 nojoin Escape Escape Escape\n")

    def test_polygon(self):
        geometry = self._DummyGeometry()

        with lines.LineFactory(geometry, "polygon") as polygon:
            polygon.new_point([0, 0])   # 1
            polygon.new_point([1, 1])   # 2
            polygon.new_point([5, 5])   # 3

            geometry.new_point([7, 0])  # 4

            polygon.new_point([6, 6])   # 5

        self.assertEqual(geometry.points[0][0], 0)
        self.assertEqual(geometry.points[0][1], 0)

        self.assertEqual(geometry.points[1][0], 1)
        self.assertEqual(geometry.points[1][1], 1)

        self.assertEqual(geometry.points[2][0], 5)
        self.assertEqual(geometry.points[2][1], 5)

        self.assertEqual(geometry.points[3][0], 7)
        self.assertEqual(geometry.points[3][1], 0)

        self.assertEqual(geometry.points[4][0], 6)
        self.assertEqual(geometry.points[4][1], 6)

        self.assertEqual(geometry.lines[0].gid_command(),
                         "Geometry Create Line join 1 2 nojoin Escape Escape Escape\n")
        self.assertEqual(geometry.lines[1].gid_command(),
                         "Geometry Create Line join 2 3 nojoin Escape Escape Escape\n")
        self.assertEqual(geometry.lines[2].gid_command(),
                         "Geometry Create Line join 3 5 nojoin Escape Escape Escape\n")
        self.assertEqual(geometry.lines[3].gid_command(),
                         "Geometry Create Line join 5 1 nojoin Escape Escape Escape\n")



