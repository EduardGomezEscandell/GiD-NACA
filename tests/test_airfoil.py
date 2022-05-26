import unittest
import numpy as np

from src.airfoil_tools import naca_generator

class TestAirfoil (unittest.TestCase):

    @classmethod
    def _read_dat(cls: type, filename: str) -> tuple:
        with open(filename, "r") as f:
            _ = f.readline()
            nupper, nlower = [int(x) for x in f.readline().replace(".", "").split()]
            assert(nupper == nlower)

            trailing_theta = float(f.readline().split(":")[-1])
            _ = f.readline()

            upper = np.zeros((nupper, 2))
            for i, line in enumerate(f):
                if i==nupper:
                    break
                upper[i, :] = [float(x) for x in line.split()]

            lower = np.zeros((nlower, 2))
            for i, line in enumerate(f):
                if i==nlower:
                    break
                lower[i, :] = [float(x) for x in line.split()]

        return nupper, upper, lower, trailing_theta

    def _RunTest(self, naca_digits: str):
        npoints, ref_upper, ref_lower, ref_theta = self._read_dat(f"tests/data/naca{naca_digits}.dat")

        _, upper_surf, lower_surf, theta = naca_generator.generate_naca(naca_digits, npoints)

        self.assertEqual(upper_surf.shape[0], npoints)
        self.assertEqual(upper_surf.shape[1], 2)

        self.assertEqual(lower_surf.shape[0], npoints)
        self.assertEqual(lower_surf.shape[1], 2)

        self.assertAlmostEqual(theta, ref_theta)

        for i,_ in enumerate(upper_surf):
            self.assertAlmostEqual(upper_surf[i, 0], ref_upper[i, 0], places=6, msg=f"Wrong X for upper point i={i}")
            self.assertAlmostEqual(upper_surf[i, 1], ref_upper[i, 1], places=6, msg=f"Wrong Y for upper point i={i}")

        for i,_ in enumerate(lower_surf):
            self.assertAlmostEqual(lower_surf[i, 0], ref_lower[i, 0], places=6, msg=f"Wrong X for lower point i={i}")
            self.assertAlmostEqual(lower_surf[i, 1], ref_lower[i, 1], places=6, msg=f"Wrong Y for lower point i={i}")

    def test_naca0012(self):
        "4-digit, symetrical"
        self._RunTest("0012")

    def test_naca2408(self):
        "4-digit, asymetrical"
        self._RunTest("2408")

