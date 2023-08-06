import unittest

# from calculate import calculate
from calc import calculator


class TestCalculator(unittest.TestCase):
    '''Testing the calculator2'''

    def setUp(self):
        '''Set up testing objects'''
        self.a = 200
        self.b = 100

    def test_add(self):
        '''Testing add menthod'''
        calculator1 = calculator.Calc(self.a, self.b)
        print(calculator1.add())
        self.assertEqual(calculator1.add(), 300)

    def test_is_not_add(self):
        '''Testing add menthod'''
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertNotEqual(calculator1.add(), 400)

    def test_sub(self):
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertEqual(calculator1.sub(), 100)

    def test_power(self):
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertNotEqual(calculator1.power(), 100)

    @unittest.skip
    def test_mul(self):
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertEqual(calculator1.mul(), 20000)

    def test_div(self):
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertEqual(calculator1.div(), 2)

    def test_mod(self):
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertEqual(calculator1.mod(), 0)

    def test_diff_int(self):
        calculator1 = calculator.Calc(self.a, self.b)
        self.assertEqual(calculator1.diff_int(), 2)



if __name__ == '__main__':
    unittest.main()

