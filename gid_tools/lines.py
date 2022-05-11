import numpy as np

class Shape1D:
    def __init__(self, geometry, append_to_geometry):
        self.parent = geometry
        if append_to_geometry:
            self.parent.lines.append(self)
            self.id = len(self.parent.lines)

    def add_point(self, coords: np.ndarray) -> int:
        raise NotImplementedError("Calling base class Shape1D.add_point()")

    def new_point(self, coords: np.ndarray) -> int:
        return self.add_point(self.parent.new_point(coords))

    def gid_command(self):
        raise NotImplementedError("Calling base class Shape1D.gid_command()")


def LineFactory(geometry, name, *args, **kwargs) -> Shape1D:
    lines = {
        "line": Line,
        "semicircle": Semicircle,
        "polygon": Polygon,
    }

    try:
        return lines[name.lower()](geometry, *args, **kwargs)
    except KeyError as e:
        print(f"Line type '{name}' not found. Try any of: {list(lines.keys())}")
        raise e


class Line(Shape1D):
    def __init__(self, parent, point1 = None, point2 = None):
        super().__init__(parent, True)
        self.points = []

        if point1 is not None:
            self.add_point(point1)
        if point2 is not None:
            self.add_point(point2)

    def add_point(self, id_: int) -> int:
        if len(self.points) >= 2:
            raise RuntimeError("Line can only have 2 control points")
        self.points.append(id_)
        return id_

    def gid_command(self):
        if len(self.points) != 2:
            print(f"WARNING: Attempting to create a Line with too few control points (has: {len(self.points)}, needs: 2).")
            return ""
        else:
            return "Geometry Create Line join {} {} nojoin Escape Escape Escape\n".format(*self.points)


class Semicircle(Shape1D):
    def __init__(self, parent):
        super().__init__(parent, True)
        self.points = []

    def add_point(self, id_: int) -> int:
        if len(self.points) >= 3:
            raise RuntimeError("Semicircle can only have 3 control points")
        self.points.append(id_)
        return id_

    def gid_command(self):
        if len(self.points) != 3:
            print(f"WARNING: Attempting to create a semicircle with too few control points (has: {len(self.points)}, needs: 3).")
            return ""
        else:
            return "Geometry Create Arc join {} {} {} nojoin Escape Escape Escape\n".format(*self.points)


class Polygon(Shape1D):
    "Creates a closed polygon with the given points"
    def __init__(self, parent):
        super().__init__(parent, False)
        self.points = []
        self.closed = False

    def add_point(self, id_: int) -> int:
        if self.closed:
            raise RuntimeError("Polygon is already closed")
        self.points.append(id_)
        if len(self.points) > 1:
            self.parent.new_1d_shape('line', self.points[-2], self.points[-1])
        return id_

    def close(self):
        if self.closed:
            return

        if len(self.points) < 3:
            raise RuntimeError("Polygon must have at least 3 points")

        self.parent.new_1d_shape('line', self.points[-1], self.points[0])
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def __del__(self):
        if not self.closed:
            print("WARNING: Polygon object deleted without closing.")