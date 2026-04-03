import unittest
from input.token import Token

class TestToken(unittest.TestCase):

    def test_construct_dest_token(self):
        destToken = Token('x', 0)
        self.assertEqual(destToken.value, 'x')
        self.assertEqual(destToken.type, 0)

    def test_construct_var_token(self):
        varToken = Token('a', 1)
        self.assertEqual(varToken.value, 'a')
        self.assertEqual(varToken.type, 1)

    def test_construct_literal_token(self):
        literalToken = Token("42", 2)
        self.assertEqual(literalToken.value, "42")
        self.assertEqual(literalToken.type, 2)

    def test_construct_op_token(self):
        opToken = Token('+', 3)
        self.assertEqual(opToken.value, '+')
        self.assertEqual(opToken.type, 3)

    def test_construct_equal_token(self):
        equalToken = Token('=', 4)
        self.assertEqual(equalToken.value, '=')
        self.assertEqual(equalToken.type, 4)

    def test_construct_live_token(self):
        liveToken = Token("live:", 5)
        self.assertEqual(liveToken.value, "live:")
        self.assertEqual(liveToken.type, 5)

if __name__ == "__main__":
    unittest.main(verbosity=2)