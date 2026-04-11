import io
from multiprocessing import Value
import unittest
from input.scanner import Scanner
from input.scanner import Token

class TestScanner(unittest.TestCase):

    def test_nextToken(self):
        input = "x = a + b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)

        self.nextToken_dest(scanner)
        self.nextToken_equal(scanner)
        self.nextToken_var(scanner)
        self.nextToken_op(scanner)
        self.nextToken_newline(scanner)
        
    def nextToken_dest(self, scanner):
        token = scanner.next_token()
        self.assertEqual(token.value, 'x')
        self.assertEqual(token.type, 0)

    def nextToken_equal(self, scanner):
        token = scanner.next_token()
        self.assertEqual(token.value, '=')
        self.assertEqual(token.type, 4)

    def nextToken_var(self, scanner):
        token = scanner.next_token()
        self.assertEqual(token.value, 'a')
        self.assertEqual(token.type, 1)

    def nextToken_op(self, scanner):
        token = scanner.next_token()
        self.assertEqual(token.value, '+')
        self.assertEqual(token.type, 3)

    def nextToken_newline(self, scanner):
        token = scanner.next_token()
        token = scanner.next_token()
        self.assertEqual(token.value, "\n")
        self.assertEqual(token.type, 7)

    def test_nextToken_EOF(self):
        try:
            file = open("./scanner_test_EOF.txt", "r")
            scanner = Scanner(file)
            token = scanner.next_token()
            self.assertEqual(token, Token("",-1))
        except:
            print("Could not open file")

    def test_nextToken_EOFLast(self):
        try:
            file = open("./scanner_test_noNewline.txt", "r")
            scanner = Scanner(file)
            for i in range(5):
                token = scanner.next_token()
            token = scanner.next_token()
            self.assertEqual(token, Token("",-1))
        except:
            print("Could not open file")

    def test_nextToken_live(self):
        input = "live:"
        file = io.StringIO(input)
        scanner = Scanner(file)
        token = scanner.next_token()
        self.assertEqual(token.value, "live:")
        self.assertEqual(token.type, 5)

    def test_nextToken_liveSymbol(self):
        input = "live:\na,"
        file = io.StringIO(input)
        scanner = Scanner(file)
        token = scanner.next_token()
        token = scanner.next_token()
        token = scanner.next_token()
        self.assertEqual(token.value, "a")
        self.assertEqual(token.type, 6)

    def test_nextToken_lit(self):
        input = "x = 42\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        token = scanner.next_token()
        token = scanner.next_token()
        token = scanner.next_token()
        self.assertEqual(token.value, "42")
        self.assertEqual(token.type, 2)
        
    def test_identify_invalidChar(self):
        input = "x$"
        file = io.StringIO(input)
        scanner = Scanner(file)
        with self.assertRaises(ValueError) as ve:
            scanner._identify(input)

    def test_identify_startWDigit(self):
        input = "1abc"
        file = io.StringIO(input)
        scanner = Scanner(file)
        with self.assertRaises(ValueError) as ve:
            scanner._identify(input)

    def test_identify_opWithSymbol(self):
        input = "a+b"
        file = io.StringIO(input)
        scanner = Scanner(file)
        with self.assertRaises(ValueError) as ve:
            scanner._identify(input)

    def test_tokenizeLine_binary(self):
        input = "x = a + b\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        scanner._tokenize_line(input)
        self.assertEqual(scanner.buffer[0].value, "x")
        self.assertEqual(scanner.buffer[0].type, 0)
        self.assertEqual(scanner.buffer[1].value, "=")
        self.assertEqual(scanner.buffer[1].type, 4)
        self.assertEqual(scanner.buffer[2].value, "a")
        self.assertEqual(scanner.buffer[2].type, 1)
        self.assertEqual(scanner.buffer[3].value, "+")
        self.assertEqual(scanner.buffer[3].type, 3)
        self.assertEqual(scanner.buffer[4].value, "b")
        self.assertEqual(scanner.buffer[4].type, 1)
        self.assertEqual(scanner.buffer[5].value, "\n")
        self.assertEqual(scanner.buffer[5].type, 7)

    def test_tokenizeLine_unary(self):
        input = "x = - a\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        scanner._tokenize_line(input)
        self.assertEqual(scanner.buffer[0].value, "x")
        self.assertEqual(scanner.buffer[0].type, 0)
        self.assertEqual(scanner.buffer[1].value,"=")
        self.assertEqual(scanner.buffer[1].type, 4)
        self.assertEqual(scanner.buffer[2].value, "-")
        self.assertEqual(scanner.buffer[2].type, 3)
        self.assertEqual(scanner.buffer[3].value, "a")
        self.assertEqual(scanner.buffer[3].type, 1)
        self.assertEqual(scanner.buffer[4].value, "\n")
        self.assertEqual(scanner.buffer[4].type, 7)

    def test_tokenizeLine_assign(self):
        input = "x = 42\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        scanner._tokenize_line(input)
        self.assertEqual(scanner.buffer[0].value, "x")
        self.assertEqual(scanner.buffer[0].type, 0)
        self.assertEqual(scanner.buffer[1].value, "=")
        self.assertEqual(scanner.buffer[1].type, 4)
        self.assertEqual(scanner.buffer[2].value, "42")
        self.assertEqual(scanner.buffer[2].type, 2)
        self.assertEqual(scanner.buffer[3].value, "\n")
        self.assertEqual(scanner.buffer[3].type, 7)

    def test_tokenizeLine_liveLine(self):
        input = "live:\n"
        file = io.StringIO(input)
        scanner = Scanner(file)
        scanner._tokenize_line(input)
        self.assertEqual(scanner.buffer[0].value, "live:")
        self.assertEqual(scanner.buffer[0].type, 5)
        self.assertEqual(scanner.buffer[1].value, "\n")
        self.assertEqual(scanner.buffer[1].type, 7)

    def test_tokenizeLine_liveSymbol(self):
        input = "live: a, b, c"
        file = io.StringIO(input)
        scanner = Scanner(file)
        tokens: list[Token] = []
        scanner._tokenize_line(input)
        self.assertEqual(scanner.buffer[0].value, "live:")
        self.assertEqual(scanner.buffer[0].type, 5)
        self.assertEqual(scanner.buffer[1].value, "a")
        self.assertEqual(scanner.buffer[1].type, 6)
        self.assertEqual(scanner.buffer[2].value, "b")
        self.assertEqual(scanner.buffer[2].type, 6)
        self.assertEqual(scanner.buffer[3].value, "c")
        self.assertEqual(scanner.buffer[3].type, 6)

    def test_readline_falseValidLine(self):
        input = "live: a, b, c"
        file = io.StringIO(input)
        scanner = Scanner(file)
        result = scanner._readline()
        self.assertEqual(result, False)

    def test_readline_trueEmptyFile(self):
        input = ""
        file = io.StringIO(input)
        scanner = Scanner(file)
        result = scanner._readline()
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main(verbosity=2)
