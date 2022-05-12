#!/usr/bin/env python3
import numpy as np

from airfoil_tools.naca_generator import generate_naca
from gid_tools.gid_geometry import Gid2DGeometry
from gid_tools.external_boundary import generate_boundary

# Data entry
naca_digits = "2412"
npoints = 100

boundary_type = "lens"
boundary_radius = 10

file_name = "naca.bch"

# Geometrty generation
geometry = Gid2DGeometry()

# Airfoil
_, upper, lower, trailing_edge_angle = generate_naca(naca_digits, npoints)

with geometry.new_1d_shape('polygon') as p:
    for point in upper[:,:]:
        p.new_point(point)
    for point in lower[-2:0:-1, :]: # Reverse order, skipping leading and trailing edges
        p.new_point(point)

# Outter boundary
generate_boundary(boundary_type, geometry, boundary_radius)

# Fluid domain
s = geometry.new_2d_shape()
for line in geometry.lines:
    s.add_line(line.id)

# GiD batch file
geometry.write(file_name)

# Useful info for enforcing free-slip condition
print(f"Trailing edge cord angle is {trailing_edge_angle} rad")
print(f"Trailing edge cord vector is [{np.cos(trailing_edge_angle)}, {np.sin(trailing_edge_angle)}]")
