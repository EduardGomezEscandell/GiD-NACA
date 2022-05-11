import numpy as np

def generate_naca(naca_code, npoints):
    # Reading name
    if len(naca_code) != 4:
        raise NotImplementedError(f"Only 4-digit NACA naca_code is implemented. Got '{naca_code}'.")

    M = int(naca_code[0]) / 100  # Max camber
    P = int(naca_code[1]) / 10   # Position of max camber
    thickness = int(naca_code[2:]) / 100

    # Generating coordinates
    camber = np.zeros(shape=(npoints, 2))
    upper_surf = np.zeros(shape=(npoints, 2))
    lower_surf = np.zeros(shape=(npoints, 2))

    for i in range(npoints):
        beta = np.pi * i/(npoints - 1)
        x = 0.5 * (1 - np.cos(beta))
        if x < P:
            y = M / P**2 * x * (2*P - x)
            grad = 2*M/P**2 * (P - x)
        else:
            y = M / (1 - P)**2 * (1 - 2*P + 2*P*x - x**2)
            grad = 2*M/(1 - P)**2 * (P - x)

        camber[i, 0] = x
        camber[i, 1] = y

        theta = np.arctan(grad)
        yt = thickness / 0.2 * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)

        upper_surf[i, 0] = x - yt * np.sin(theta)
        upper_surf[i, 1] = y + yt * np.cos(theta)

        lower_surf[i, 0] = x + yt * np.sin(theta)
        lower_surf[i, 1] = y - yt * np.cos(theta)

    return camber, upper_surf, lower_surf

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    naca_code = '4412'
    camber, upper, lower = generate_naca(naca_code, 100)

    plt.title(f'NACA {naca_code}')
    plt.plot(camber[:, 0], camber[:, 1], label='Camber')
    plt.plot(upper[:, 0], upper[:, 1], label='Upper surface')
    plt.plot(lower[:, 0], lower[:, 1], label='Lower surface')
    plt.axis('equal')
    plt.legend()
    plt.show()