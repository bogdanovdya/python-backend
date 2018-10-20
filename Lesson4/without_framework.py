import math
import gcd


def test_gcd(a, b):
    if gcd.gcd(a, b) == math.gcd(a, b):
        pass
    else:
        print("Test gcd(", a, ",", b, ") is Fail")


if __name__ == "__main__":
    for i in range(0, 101, 1):
        for j in range(0, 101, 1):

            test_gcd(i, j)
