import unittest
import math
import gcd


class CalcTest(unittest.TestCase):
    def test_gcd(self):
        for i in range(0, 30, 1):
            for j in range(0, 30, 1):
                with self.subTest(i=i, j=j):
                    self.assertEqual(gcd.gcd(i, j), math.gcd(i, j))


if __name__ == '__main__':
    unittest.main()
