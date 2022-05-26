import unittest

from tests import  test_airfoil
from tests import  test_lines

def assemble_test_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromModule(test_airfoil))
    suite.addTests(unittest.TestLoader().loadTestsFromModule(test_lines))
    return suite
