import unittest
from tests.tests import assemble_test_suite

runner = unittest.TextTestRunner()
runner.run(assemble_test_suite())