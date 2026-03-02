import io
from multiprocessing import Value
import unittest
from input.scanner import Scanner
from input.scanner import Token

class TestScanner(unittest.TestCase):

    def test_reset(self):
        """
            Tests the scanner.reset() function to ensure it is clearing
            the token index and buffer.
        """
        input = "a = a + 1\nt1 = a * 4\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try: 
            scanner._readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")

        # Call function we want to test
        scanner._reset()

        self.assertEqual(scanner.index, 0)
        self.assertEqual(scanner.buffer, [])

    def test_next_token(self):
        input = "a = a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try:
            scanner._readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")

        tokens_read = []
        for i in range(len(scanner.buffer) - 1):
            tokens_read.append(scanner.next_token())
            # If the next token is equal to the token we just read, next_tokens()
            # is not working
            self.assertNotEqual(scanner.next_token(), tokens_read[i])
            
    def test_identify_case1(self):
        """
            Tests the identify method of Scanner by simulating a file input.
            Only tests for valid input cases.
        """

        input = "a = a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try:
            scanner._readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")

        # destination, equals, variable, operator, literal, newline
        expected = [0,4,1,3,2,7]
        received = []
        for symbol in scanner.buffer:
            received.append(symbol.type)
        
        self.assertEqual(received, expected)

        scanner._reset()

    def test_identify_case2(self):
        """
            Tests the identify method of Scanner by simulating a file input.
            Only tests for valid input cases.
        """
        
        input = "t1 = a* 4\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try:
            scanner._readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")    
        
        # destination, equals, variable, operator, literal, newline
        expected = [0,4,1,3,2,7]
        received = []
        for symbol in scanner.buffer:
            received.append(symbol.type)
        
        self.assertEqual(received, expected)

        scanner._reset()

    def test_identify_invalid_input1(self):

        input = "a ] a $ 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        # This test should pass if the scanner.identify() method properly raises an error
        with self.assertRaises(ValueError) as cm:
            scanner._identify(input)

    def test_identify_invalid_input2(self):

        input = "a a = 1 + 2\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        # This test should pass if the scanner.identify() method properly raises an error
        with self.assertRaises(ValueError) as cm:
            scanner._identify(input)
            print(cm)

    def test_identify_invalid_input3(self):

        input = "a = b - c = d\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        # This test should pass if the scanner.identify() method properly raises an error
        with self.assertRaises(ValueError) as cm:
            scanner._identify(input)

        scanner._reset()

    def test_readline_invalid_input1(self):
        input = "a ] a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        with self.assertRaises(ValueError) as ve:
            scanner._readline()

        scanner._reset()

    def test_tokenize_line1(self):
        input = "a = a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        scanner._tokenize_line(input)
        
        token_list: list[str] = []
        for token in scanner.buffer:
            token_list.append(token.value)

        self.assertEqual(token_list[0], "a")
        self.assertEqual(token_list[1], "=")
        self.assertEqual(token_list[2], "a")
        self.assertEqual(token_list[3], "+")
        self.assertEqual(token_list[4], "1")
        self.assertEqual(token_list[5], "\n")

    def test_tokenize_line2(self):
        input = "t1 = a * 4\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        scanner._tokenize_line(input)
        
        token_list: list[str] = []
        for token in scanner.buffer:
            token_list.append(token.value)

        self.assertEqual(token_list[0], "t1")
        self.assertEqual(token_list[1], "=")
        self.assertEqual(token_list[2], "a")
        self.assertEqual(token_list[3], "*")
        self.assertEqual(token_list[4], "4")
        self.assertEqual(token_list[5], "\n")

    def test_tokenize_line3(self):
        input = "t1 / a + 3\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        scanner._tokenize_line(input)

        token_list: list[str] = []
        for token in scanner.buffer:
            token_list.append(token.value)

        self.assertEqual(token_list[0], "t1")
        self.assertEqual(token_list[1], "/")
        self.assertEqual(token_list[2], "a")
        self.assertEqual(token_list[3], "+")
        self.assertEqual(token_list[4], "3")
        self.assertEqual(token_list[5], "\n")

    def test_multiline_to_eof(self):
        '''
        tests that next_token() correctly hits end of file after multiple lines of input.
        '''
        input = "a = 1\nb = 2\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        # Should be 8 tokens
        tokens = []
        for i in range(8):
            tokens.append(scanner.next_token().type)
        
        # Check that 9th call returns EOF
        self.assertEqual(scanner.next_token().type, -1)

    def test_liveness_transition(self):
        '''
        Tests that the identify() function identifies 'live' keyword properly
        '''
        input = "live: a, b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        token = scanner.next_token()

        self.assertEqual(scanner.reading, "live")

        next_token = scanner.next_token() # This should be 'a'
        self.assertEqual(next_token.type, 6)

    def test_invalid_identifier_start(self):
        '''
        Ensures any destination that starts with a number will raise a value error. (i.e. 1a = 2 is not valid)
        '''
        input = "1a = 2\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        with self.assertRaises(ValueError):
            scanner._identify("1a")

    def test_destination_variable(self):
        '''
        Ensures the first sequence is 'destination' (type=0) and others are variable (type=1)
        '''
        input = "res = a + b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        scanner._readline()

        self.assertEqual(scanner.buffer[0].type, 0)
        self.assertEqual(scanner.buffer[2].type, 1)
        self.assertEqual(scanner.buffer[4].type, 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
