import unittest

# from calculate import calculator
from program2.calculator import calc


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

    @unittest.skip
    def test_is_not_add(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.add())
        self.assertNotEqual(calculator.add(), 300)

    def test_mod(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.add())
        self.assertEqual(calculator.mod(), 0)