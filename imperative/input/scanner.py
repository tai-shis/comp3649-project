from typing import TextIO

class Token:
    # Reference dict for types
    types = {
        0: "destination",  # 'd', 't3', 'z', destination (variable)
        1: "variable",     # 'a', 't1', 'b', variables
        2: "literal",      # '1', '23', '415', any integer literal
        3: "operator",     # '+', '-', '*', '/' operators
        4: "equals",       # '=' occurs once
        5: "live",         # 'live:' occurs once
        6: "live_symbol",  # 'a,', 'c,', 'd,', etc... (excluding commas in tokens)
        7: "newline",      # '\n', terminating character   
        -1: "EOF"          # End of File
    }

    def __init__(self, value: str, type: int):
        self.value: str = value
        self.type: int = type

    def type_string(self):
        """
            Returns the human-readable representation of the
            token's type.
        """

        return self.types[self.type]

    def __str__(self):
        return f"{repr(self.value)}: {self.type_string()}"

class Scanner:
    # List of allowed operators
    operators = ['+', '-', '*', '/']

    # List of invalid characters (can change)
    invalid = [
        '$', '`', '"', '\'', '\\', '&', '^', '%', '#', '@', '!', '~', 
        '_', '[', ']', '{', '}', '|', ';', '<', '>', '?'
    ]

    # I know it's duplicated, but it's so there are no magic numbers
    types = {
        'destination': 0,  # ex. 'd', 't3', 'z', destination (variable)
        'variable': 1,     # ex. 'a', 't1', 'b', variables
        'literal': 2,      # ex. '1', '23', '415', any integer literal
        'operator': 3,     # '+', '-', '*', '/' operators
        'equals': 4,       # '=' occurs once
        'live': 5,         # 'live:' occurs once
        'live_symbol': 6,  # ex. 'a,', 'c,', 'd,', etc... (excluding commas in tokens)
        'newline': 7,      # '\n', terminating character
        'EOF': -1          # End of File
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

    def reset(self):
        """
            Reset the scanner's internal state, excluding the input stream
        """
        self.index = 0
        self.buffer = []
        self.reading = "instructions"

    def identify(self, symbol: str) -> int:
        """
            Identifies the given object/string into it's tokenized 'type'.

            :return: Identified type as an integer.
            :rtype: int
            :raises ValueError: If the symbol contains invalid characters.
        """

        if symbol == '\n':
            return self.types["newline"]

        if symbol == '=':
            return self.types["equals"]

        # If our symbol is just numbers, it's a literal
        if symbol.isdigit():
            return self.types["literal"]
        # If symbol is in the list of operators, it returns true.
        # If it's just "symbol in operators", it returns true for something like "+" in "+t"
        if any(op == symbol for op in self.operators):
            return self.types["operator"]

        if symbol == 'live:':
            # we have read in a live, switch state
            self.reading = "live"
            return self.types["live"]

        if self.reading == "live":
            return self.types["live_symbol"]
        
        # If the symbol is not any of the above, it's probably a variable; first check for invalid characters
        # if theres an invalid character, reject; if theres an operator with other stuff; also reject 
        # (this won't catch singletons because singletons are already handled above)
        if any(char in symbol for char in self.invalid) or any(op in symbol for op in self.operators):
            raise ValueError(f"Invalid character in symbol: {symbol}")

        # If a symbol starting with a number is valid, comment the following check:
        if symbol[0].isdigit():
            raise ValueError(f"Invalid symbol starting with number: {symbol}")

        # Otherwise, it's a valid variable/destination
        return self.types["destination"] if len(self.buffer) == 0 else self.types["variable"] 

    def tokenize(self, symbol: str) -> Token:
        """
            Tokenizes the given symbol into a Token object if valid.

            
            :param symbol: Read in symbol to be tokenized
            :type symbol: str
            :return: Identified symbol as a Token, if valid
            :rtype: Token
            :raises ValueError: If the symbol contains invalid characters.

        """
        try: 
            type: int = self.identify(symbol)
        except ValueError as ve:
            raise 

        return Token(symbol, type)

    def readline(self) -> bool:
        """
            Tokenizes a line of the input into a list of tokens in the internal buffer.
            Error checking for valid order of tokens is not done. However, valid characters
            should be checked when obtaining the type.

            :return: True if EOF, False otherwise.
            :rtype: bool

            :raises ValueError: If the read line contains invalid characters.
        """
        
        # get leading whitespace out so we can assume we are reading destination immediately
        line = self.file.readline().lstrip()

        if line == '':
            return True
        
        # Before anything, reset buffer and index
        self.buffer: list[Token] = []
        self.index: int = 0

        symbol: str = ""
        read_cur: bool = False # False while reading a symbol; True when between symbols looking for the next one

        for char in line:            
            if char in self.operators or char in ['\n', '=', ',']:  # Catch weird cases (newline or operator/equals)
                # Tokenize what we have, if it exists
                try:
                    if symbol:
                        self.buffer.append(self.tokenize(symbol))
                        symbol = ""

                    # Then, we tokenize the operator (as long as it's not a comma)
                    if char != ',':
                        self.buffer.append(self.tokenize(char))
                    read_cur = True
                except ValueError as ve:
                    raise
            elif not read_cur: # Currently reading a new symbol
                if char == ' ': # Symbol is ended by a space, so tokenize
                    try:
                        self.buffer.append(self.tokenize(symbol))
                    except ValueError as ve:
                        raise

                    read_cur = True
                    symbol = ""
                else:
                    symbol += char
            else: # Searching for new symbol
                if char != ' ':
                    symbol += char
                    read_cur = False

        # Make sure to tokenize anything left over at the end of the file
        try:
            if symbol:
                self.buffer.append(self.tokenize(symbol))
        except ValueError as ve:
            raise

        return False

    def next_token(self) -> Token:
        """
            Get the next token from the input stream, until all characters are read
 
            :return: Next token from the input stream. EOF token when input stream is exhausted.
            :rtype: Token
            :raises ValueError: If the input stream contains invalid characters.
        """
        if len(self.buffer) - 1 == self.index or len(self.buffer) == 0:
            try:
                if (self.readline()): # EOF reached
                    return Token("", -1) # return EOF token
            except ValueError as ve:
                raise
        else:
            self.index += 1

        return self.buffer[self.index]

        
