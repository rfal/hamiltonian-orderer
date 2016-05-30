import unittest
from orderer import *

class TestSymbol(unittest.TestCase):
    pass

class TestTerm(unittest.TestCase):
    pass

class TestExpression(unittest.TestCase):
    pass


if __name__ == '__main__':
    print(">>> Testing Symbol class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSymbol)
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("\n======================================================================\n")

    print(">>> Testing Term class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTerm)
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("\n======================================================================\n")
    
    print(">>> Testing Expression class...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpression)
    unittest.TextTestRunner(verbosity=2).run(suite)