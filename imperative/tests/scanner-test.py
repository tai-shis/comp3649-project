import io
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
            scanner.readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")

        # Call function we want to test
        scanner.reset()

        self.assertEqual(scanner.index, 0)
        self.assertEqual(scanner.buffer, [])

    def test_next_tokens(self):
        input = "a = a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try:
            scanner.readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")

        tokens_read = []
        for i in range(len(scanner.buffer) - 1):
            tokens_read.append(scanner.next_tokens())
            # If the next token is equal to the token we just read, next_tokens()
            # is not working
            self.assertNotEqual(scanner.next_tokens(), tokens_read[i])
            
    def test_identify_case1(self):
        """
            Tests the identify method of Scanner by simulating a file input.
            Only tests for valid input cases.
        """

        input = "a = a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try:
            scanner.readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")

        # destination, equals, variable, operator, literal, newline
        expected = [0,4,1,3,2,7]
        received = []
        for symbol in scanner.buffer:
            received.append(symbol.type)
        
        self.assertEqual(received, expected)

        scanner.reset()

    def test_identify_case2(self):
        """
            Tests the identify method of Scanner by simulating a file input.
            Only tests for valid input cases.
        """
        
        input = "t1 = a* 4\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        try:
            scanner.readline()
        except ValueError as ve:
            print(f"Error during readline: {ve}")    
        
        # destination, equals, variable, operator, literal, newline
        expected = [0,4,1,3,2,7]
        received = []
        for symbol in scanner.buffer:
            received.append(symbol.type)
        
        self.assertEqual(received, expected)

        scanner.reset()

    def test_identify_invalid_input1(self):

        input = "a \ a $ 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        # This test should pass if the scanner.identify() method properly raises an error
        with self.assertRaises(ValueError) as cm:
            scanner.identify(input)

    def test_identify_invalid_input2(self):

        input = "a a = 1 + 2\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        # This test should pass if the scanner.identify() method properly raises an error
        with self.assertRaises(ValueError) as cm:
            scanner.identify(input)
            print(cm)

    def test_identify_invalid_input3(self):

        input = "a = b - c = d\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        
        # This test should pass if the scanner.identify() method properly raises an error
        with self.assertRaises(ValueError) as cm:
            scanner.identify(input)

    def test_readline_invalid_input1(self):
        input = "a \ a + 1\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        with self.assertRaises(ValueError) as ve:
            scanner.readline()


if __name__ == '__main__':
    unittest.main(verbosity=2)
