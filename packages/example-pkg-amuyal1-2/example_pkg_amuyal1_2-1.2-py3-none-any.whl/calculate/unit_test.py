import unittest

# from calculate import calculate
from program.calculate import calc


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

    def test_is_not_add(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.add())
        self.assertNotEqual(calculator.add(), 400)

    def test_sub(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.sub())
        self.assertEqual(calculator.sub(), 100)

    def test_power(self):
        calculator = calc.Calc(self.a, self.b)
        self.assertNotEqual(calculator.power(), 100)

    def test_mul(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.mul())
        self.assertEqual(calculator.mul(), 20000)

    def test_div(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.div())
        self.assertEqual(calculator.div(), 2)
#    @unittest.skip

    def test_mod(self):
        calculator = calc.Calc(self.a, self.b)
        self.assertEqual(calculator.mod(), 0)

    def test_diff_int(self):
        calculator = calc.Calc(self.a, self.b)
        self.assertEqual(calculator.diff_int(), 2)

    def test_special_character(self):
        '''Testing add menthod'''
        calculator = calc.Calc(self.a, self.b)
        print(calculator.add())
        self.assertTrue(calculator.add(), "300")

if __name__ == '__main__':
    unittest.main()