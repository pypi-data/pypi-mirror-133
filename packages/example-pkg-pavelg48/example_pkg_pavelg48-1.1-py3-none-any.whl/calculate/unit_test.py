# import unittest
#
#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()

import unittest

# from calculate import calc
from calculator import calc


class TestCalculator(unittest.TestCase):
    '''Testing the calculator2'''

    def setUp(self):
        '''Set up testing objects'''
        self.a = 200
        self.b = 100

    def test_add(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.add())
        self.assertEqual(calculator.add(), 300)

    def test_special_character(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.add())
        self.assertTrue(calculator.add(), "300")


if __name__ == '__main__':
    unittest.main()
