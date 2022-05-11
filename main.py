from airfoil_tools.naca_generator import generate_naca
from gid_tools.gid_geometry import Gid2DGeometry
from gid_tools.external_boundary import generate_boundary

# Data entry
naca_digits = "0012"
file_name = "naca0012.bch"
npoints = 100
shell_radius = 10

# Geometrty generation
geometry = Gid2DGeometry()

# Airfoil
_, upper, lower = generate_naca(naca_digits, npoints)

with geometry.new_1d_shape('polygon') as p:
    for point in upper[:,:]:
        p.new_point(point)
    for point in lower[-2:0:-1, :]: # Reverse order, skipping leading and trailing edges
        p.new_point(point)

# Outter boundary
generate_boundary("lens", geometry, shell_radius)

# Fluid domain
s = geometry.new_2d_shape()
for line in geometry.lines:
    s.add_line(line.id)

# GiD batch file
geometry.write(file_name)
