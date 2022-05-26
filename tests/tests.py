import unittest

from tests import  test_airfoil

def assemble_test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromModule(test_airfoil))
    return suite
