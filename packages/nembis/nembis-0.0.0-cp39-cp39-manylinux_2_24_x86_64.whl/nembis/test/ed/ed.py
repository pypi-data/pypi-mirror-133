import unittest

from nembis.cpp.ed import *

class TestOperator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #print("A class method called before tests in an individual class are run.\n")
        pass

    @classmethod
    def tearDownClass(cls):
        #print("A class method called after tests in an individual class have run.\n")
        pass

    def setUp(self):
        #print("Method called to prepare the test fixture.\n")
        pass

    def tearDown(self):
        #print("Method called immediately after the test method has been called and the result recorded.\n")
        pass

    def test_operator(self):
        print("\n")
        a = OperatorReal()
        b = OperatorReal()
        a.set_size(3, 3)
        b.set_size(3, 3)
        a.set(0, 0, 1.0)
        b.ones()

        a.print()
        b.print()

        self.assertTrue(abs(a.get(0, 0) - 1.0) < 1.0e-6)

class TestBasis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #print("A class method called before tests in an individual class are run.\n")
        pass

    @classmethod
    def tearDownClass(cls):
        #print("A class method called after tests in an individual class have run.\n")
        pass

    def setUp(self):
        #print("Method called to prepare the test fixture.\n")
        pass

    def tearDown(self):
        #print("Method called immediately after the test method has been called and the result recorded.\n")
        pass

    def test_basis(self):
        print("\n")
        a = BasisReal()
        b = BasisReal()
        a.set_size(3)
        b.set_size(3)
        a.set(0, 1.0)
        b.ones()

        a.print()
        b.print()

        self.assertTrue(abs(a.get(0) - 1.0) < 1.0e-6)

if __name__ == '__main__':
    unittest.main(verbosity=1)
