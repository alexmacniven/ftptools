import unittest

from package.api import Api


class TestApi(unittest.TestCase):
    def test_funcname_raises(self):
        with self.assertRaises(NotImplementedError):
            Api.funcname()


if __name__ == "__main__":
    unittest.main()
