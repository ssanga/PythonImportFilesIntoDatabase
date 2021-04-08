
from operations import Operations
from unittest.mock import MagicMock
import unittest

# https://docs.python.org/3/library/unittest.mock.html
class OperationsTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_sum(self):
        sut = Operations()
        sut.sum = MagicMock(return_value=3)
        result = sut.sum(1,1)
        self.assertEqual(result,3)

    

       
    
         
    

