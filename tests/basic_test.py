"""
Unit Tests
"""

import unittest


class HelloWorld_test(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(1 + 1, 2)


if __name__ == "__main__":
    unittest.main()
