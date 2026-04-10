from typing import TextIO
from input.token import Token

class Scanner:
    operators = ['+', '-', '*', '/']

    invalid = [
        '$', '`', '"', '\'', '\\', '&', '^', '%', '#', '@', '!', '~', 
        '_', '[', ']', '{', '}', '|', ';', '<', '>', '?'
    ]

    types = {
        'destination': 0,  # ex. 'd', 't3', 'z', destination (variable)
        'variable': 1,     # ex. 'a', 't1', 'b', variables
        'literal': 2,      # ex. '1', '23', '415', any integer literal
        'operator': 3,     # '+', '-', '*', '/' operators
        'equals': 4,
        'live': 5,         # 'live:' occurs once
        'live_symbol': 6,  # ex. 'a,', 'c,', 'd,', etc... (excluding commas in tokens)
        'newline': 7,
        'EOF': -1
    }

    def __init__(self, file: TextIO):  
        self.file: TextIO = file

        # State on what we are reading
        self.reading: str = "instructions"  # instructions or live

        # Scanner should hold the read line and which token it is passing
        self.index: int = 0 # to avoid shifting and quicker checks
        self.buffer: list[Token] = [] # maxmimum length O(1) (max 6)

    def __str__(self):
        return f"index: {self.index}, buffer: {[str(token) for token in self.buffer]}"

    def _reset(self):
        """Resets the scanner's internal state, excluding the input stream."""
        self.index = 0
        self.buffer = []
        self.reading = "instructions"

    def _identify(self, symbol: str) -> int:
        """
        Identifies the given symbol into its tokenized type.

        :return: Identified type as an integer.
        :rtype: int
        :raises ValueError: If the symbol contains invalid characters.
        """

        if symbol == '\n':
            return self.types["newline"]

        if symbol == '=':
            return self.types["equals"]

        if symbol.isdigit():
            return self.types["literal"]
        
        if any(op == symbol for op in self.operators):
            return self.types["operator"]

        if symbol == 'live:':
            self.reading = "live"
            return self.types["live"]

        if self.reading == "live":
            return self.types["live_symbol"]
        
        # symbol is likely a variable at this point. Check for invalids/operators and reject if true
        if any(char in symbol for char in self.invalid) or any(op in symbol for op in self.operators):
            raise ValueError(f"Invalid character in symbol: {symbol}")

        if symbol[0].isdigit():
            raise ValueError(f"Invalid symbol starting with number: {symbol}")

        # Otherwise, it's a valid variable/destination
        return self.types["destination"] if len(self.buffer) == 0 else self.types["variable"] 

    def _tokenize(self, symbol: str) -> Token:
        """
        Tokenizes the given symbol into a Token object if valid.

        :param symbol: Symbol to be tokenized.
        :type symbol: str
        :return: Identified symbol as a Token.
        :rtype: Token
        """
        type: int = self._identify(symbol)

        return Token(symbol, type)

    def _readline(self) -> bool:
        """
        Tokenizes a line of the input into a list of tokens in the internal buffer.
        Token order is not validated here; character validity is checked during type identification.

        :return: True if EOF, False otherwise.
        :rtype: bool
        """
        
        # Leading whitespace increases time to tokenize, get rid of it
        line = self.file.readline().lstrip()

        # Hit EOF
        if line == '':
            return True
        
        # Before anything, reset buffer and index
        self.buffer: list[Token] = []
        self.index: int = 0

        self._tokenize_line(line)

        return False

    def _tokenize_line(self, line: str):
        symbol = ""
        delimiters = {'\n', '=', ',', ' '}
            
        for char in line:
            if char in delimiters or char in self.operators:
                # Make sure a symbol is present and tokenize it
                if symbol != "":
                    self.buffer.append(self._tokenize(symbol))
                    # Reset before building next symbol
                    symbol = "" 
                
                # As long as there are no invalid symbols, space (' '), or commas here, we can tokenize it.
                if char not in self.invalid and char not in (' ', ','):
                    self.buffer.append(self._tokenize(char))

            else: # Have not reached end of symbol
                symbol += char
        
        # Make sure to catch anything left over at the end of the line
        if symbol:
            self.buffer.append(self._tokenize(symbol))

    def next_token(self) -> Token:
        """
        Returns the next token from the input stream.

        :return: Next token from the input stream, or an EOF token when exhausted.
        :rtype: Token
        """
        if len(self.buffer) - 1 == self.index or len(self.buffer) == 0:
            if (self._readline()): # EOF reached
                return Token("", -1)
        else:
            self.index += 1

        return self.buffer[self.index]

        
