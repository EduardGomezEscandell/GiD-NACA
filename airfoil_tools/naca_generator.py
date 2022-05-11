import numpy as np

from airfoil_tools.naca_impl import NACAFactory

def generate_naca(naca_code, npoints):
    # Reading name
    airfoil = NACAFactory(naca_code)

    # Generating coordinates
    camber = np.zeros(shape=(npoints, 2))
    upper_surf = np.zeros(shape=(npoints, 2))
    lower_surf = np.zeros(shape=(npoints, 2))

    for i in range(npoints):
        beta = np.pi * i/(npoints - 1)
        x = 0.5 * (1 - np.cos(beta))
        y = airfoil.camber(x)

        camber[i, 0] = x
        camber[i, 1] = y

        theta = np.arctan(airfoil.gradient(x))
        yt = airfoil.thickness(x)

        upper_surf[i, :] = airfoil.upper_surface(x, y, yt, theta)
        lower_surf[i, :] = airfoil.lower_surface(x, y, yt, theta)

    return camber, upper_surf, lower_surf
