import pytest
import math
import gcd


def test_gcd(a, b):
    assert gcd.gcd(a, b) == math.gcd(a, b)


class TestClass:
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')