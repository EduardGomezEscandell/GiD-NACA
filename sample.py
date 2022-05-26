from src import generate_airfoil


# Data entry
naca_digits = "0012"        # The airfoil to generate
npoints = 100               # Number of points in each surface of the airfoil

boundary_type = "lens"      # The type of fluid domain. Use "none" to generate only the airfoil
boundary_radius = 10        # The size of the fluid domain

file_name = "naca.bch"      # The file to store the domain in

generate_airfoil.generate_airfoil(naca_digits, npoints, boundary_type, boundary_radius, file_name)