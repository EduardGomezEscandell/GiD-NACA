import numpy as np
from gid_tools.lines import LineFactory, Polygon, Shape1D
from gid_tools.surfaces import NurbsSurface

class Gid2DGeometry:
    def __init__(self):
        self.points = []
        self.lines = []
        self.surfaces = []

    def new_point(self, coords: np.ndarray) -> int:
        "Creates a new point and returns its id"
        self.points.append(np.array(coords))
        return len(self.points)

    def new_1d_shape(self, type, *args, **kwargs) -> Shape1D:
        "Creates a new shape with a single degree of freedom: Lines, Semicircles, and (hollow) Polygons"
        return LineFactory(self, type, *args, **kwargs)

    def new_2d_shape(self) -> NurbsSurface:
        "Creates a new shape with two degree of freedom: NurbsSurfaces"
        return NurbsSurface(self)

    def write(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for point in self.points:
                f.write("Geometry Create Point {} {} 0.0 Escape Escape Escape\n".format(*point))
            for line in self.lines:
                f.write(line.gid_command())
            for surf in self.surfaces:
                f.write(surf.gid_command())