import unittest

from nembis.cpp.utils import version


class TestVersion(unittest.TestCase):
    """Test cpp.version """

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

    def test_version(self):
        """Test method version"""
        self.assertTrue(version() == "0.0.0")

if __name__ == '__main__':
    unittest.main(verbosity=1)
