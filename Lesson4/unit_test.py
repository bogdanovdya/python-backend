import unittest
import math
import gcd


class CalcTest(unittest.TestCase):
    def test_add(self):
        for i in range(0, 101, 1):
            for j in range(0, 101, 1):
                self.assertEqual(gcd.gcd(i, j), math.gcd(i, j))


if __name__ == '__main__':
    unittest.main()