import numpy as np

class NACA:
    def __init__(self, naca_code: str):
        self.T = int(naca_code[-2:]) / 100

    def camber(self, x: float) -> float:
        raise NotImplementedError("Calling virtual method NACA.camber().")

    def gradient(self, x: float) -> float:
        raise NotImplementedError("Calling virtual method NACA.gradient().")

    def thickness(self, x: float) -> float:
        return self.T / 0.2 * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1036*x**4)

    def upper_surface(self, x: float, y: float, yt: float, theta: float) -> float:
        return np.array([
            x - yt * np.sin(theta),
            y + yt * np.cos(theta)
        ])

    def lower_surface(self, x: float, y: float, yt: float, theta: float) -> float:
        return np.array([
            x + yt * np.sin(theta),
            y - yt * np.cos(theta)
        ])

def NACAFactory(naca_code) -> NACA:
    available = {
        4: NACAFourDigit,
        5: NACAFiveDigit,
    }

    try:
        return available[len(naca_code)](naca_code)
    except KeyError as e:
        raise KeyError(f"NACA codes with {len(naca_code)} digits are not implemented.") from e

class NACAFourDigit(NACA):
    def __init__(self, naca_code):
        super().__init__(naca_code)
        assert len(naca_code) == 4
        self.M = int(naca_code[0]) / 100  # Max camber
        self.P = int(naca_code[1]) / 10   # Position of max camber

    def camber(self, x) -> float:
        if x < self.P:
            return self.M / self.P**2 * x * (2*self.P - x)
        return self.M / (1 - self.P)**2 * (1 - 2*self.P + 2*self.P*x - x**2)

    def gradient(self, x) -> float:
        if x < self.P:
            return 2*self.M/self.P**2 * (self.P - x)
        else:
            return 2*self.M/(1 - self.P)**2 * (self.P - x)

class NACAFiveDigit(NACA):
    STANDARD = 0
    REFLEX = 1

    def __init__(self, naca_code):
        super().__init__(naca_code)
        assert len(naca_code) == 5
        self.CL = int(naca_code[0]) * 3/20    # Lift coefficient
        self.P = int(naca_code[1])
        self.r = self.P / 20       # Position of max camber

        self.camber_type = int(naca_code[2])  # Standard vs. reflex
        assert self.camber_type in [self.STANDARD, self.REFLEX]

        self._compute_constants()

    def _compute_constants(self) -> None:
        if self.camber_type == self.STANDARD:
            if self.P < 1 or self.P > 5:
                raise ValueError(f"Data available only for NACA xP0xx with P between 1 and 5. Got {self.P}.")
            self.M = [0.0, 0.0580, 0.128, 0.2025, 0.29, 0.391][self.P]
            self.k1 = [0.0, 361.4, 51.64, 15.957, 6.643, 3.230][self.P]
        else:
            if self.P < 2 or self.P > 5:
                raise ValueError(f"Data available only for NACA xP1xx with P between 2 and 5. Got {self.P}.")
            self.M = [0.0, 0.0, 0.13, 0.2170, 0.3180, 0.4410][self.P]
            self.k1 = [0.0, 0.0, 51.990, 15.793, 6.520, 3.191][self.P]
            self.ratio = (3*(self.M - self.r)**2 - self.M**3) / (1 - self.M)**3

            print(self.M)
            print(self.k1)
            print(self.ratio)

    def _standard_camber(self, x) -> float:
        r = self.r
        if x < r:
            return self.k1/6 * (x**3 - 3*r*x**2 + r**2*(3-r)*x)
        return self.k1*r**3/6 * (1 - x)

    def _reflex_camber(self, x) -> float:
        r = self.r
        ratio = self.ratio
        m = self.M
        if x < r:
            return self.k1/6*((x - m)**3 - ratio*(1 - m)**3*x - m**3*x + m**3)
        return self.k1/6*(ratio*(x - m)**3 - ratio*(1 - m)**3*x - m**3*x + m**3)

    def _standard_gradient(self, x) -> float:
        r = self.r
        if x < r:
            return self.k1/6*(3*x**2 - 6*r*x + r**2*(3-r))
        else:
            return - self.k1*r**3/6*(1 - x)

    def _reflex_gradient(self, x) -> float:
        r = self.r
        ratio = self.ratio
        m = self.M
        if x < r:
            return self.k1/6*(-m**3 - ratio*(1 - m)**3 + 3*(-m + x)**2)
        return self.k1/6*(-m**3 - ratio*(1 - m)**3 + 3*ratio*(-m + x)**2)

    def camber(self, x) -> float:
        if self.camber_type == self.STANDARD:
            return self._standard_camber(x)
        else:
            return self._reflex_camber(x)

    def gradient(self, x) -> float:
        if self.camber_type == self.STANDARD:
            return self._standard_gradient(x)
        else:
            return self._reflex_gradient(x)
