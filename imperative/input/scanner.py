from typing import TextIO

class Token:
    def __init__(self, value: str, type: int):
        self.value: str = value
        self.type: int = type

    def type_string(self):
        """
            Returns the human-readable representation of the
            token's type.
        """

         # Reference dict for types
        types = {
            0: "destination",  # 'd', 't3', 'z', destination (variable)
            1: "variable",     # 'a', 't1', 'b', variables
            2: "literal",      # '1', '23', '415', any integer literal
            3: "operator",     # '+', '-', '*', '/' operators
            4: "equals",       # '=' occurs once
            5: "live",         # 'live:' occurs once
            6: "live_symbol",  # 'a:', 'c:', 'd:', etc...
            7: "newline"       # '\n', terminating character   
        }

        return types[self.type]

    def __str__(self):
        return f"{repr(self.value)}: {self.type_string()}"

class Scanner:
    # Invalid Characters
    invalid = [

    ]

    def __init__(self, file: TextIO):  
        self.file: TextIO = file

        # # What the scanner is reading (instruction):
        # # 0: instructions, 1: live objects  
        # self.state: int = 0 

        # Scanner should hold the read line and which token it is passing
        self.index: int = 0 # to avoid shifting and quicker checks
        self.buffer: list[Token] = [] # maxmimum length O(1) (max 6)

    def __str__(self):
        return f"index: {self.index}, buffer: {[str(token) for token in self.buffer]}"

    def reset(self):
        self.index = 0
        self.buffer = []

    def identify(self, symbol: str):
        """
            Identifies the given object/string into its tokenized 'type'.

            This method should be called in a try/catch block.
        """
        
        # I know its duplicated, but its so there are no magic numbers
        types = {
            'destination': 0,  # ex. 'd', 't3', 'z', destination (variable)
            'variable': 1,     # ex. 'a', 't1', 'b', variables
            'literal': 2,      # ex. '1', '23', '415', any integer literal
            'operator': 3,     # '+', '-', '*', '/' operators
            'equals': 4,       # '=' occurs once
            'live': 5,         # 'live:' occurs once
            'live_symbol': 6,  # ex. 'a,', 'c,', 'd,', etc...
            'newline': 7       # '\n', terminating character
        }

        # List of allowed operators
        operators = ['+', '-', '*', '/']

        # List of invalid characters (can change)
        invalid = [
            '$', '`', '"', '\'', '\\', '&', '^', '%', '#', '@', '!', '~', 
            '_', '[', ']', '{', '}', '|', ';', '<', '>', '?'
        ]

        if symbol == '=':
            return types["equals"]

        # If our symbol is just numbers, its a literal
        if symbol.isdigit():
            return types["literal"]

        # If symbol is in the list of operators, it returns true.
        # If its just "symbol in operators", it returns true for something like "+" in "+t"
        if any(op == symbol for op in operators):
            return types["operator"]

        if symbol == 'live:':
            return types["live"]

        if symbol.endswith(','):
            return types["live_symbol"]
        
        # If the symbol is not any of the above, its probably a variable; first check for invalid characters
        # if theres an invalid character, reject; if theres an operator with other stuff; also reject 
        # (this won't catch singletons because singletons are already handled above)
        if any(char in symbol for char in invalid) or any(op in symbol for op in operators):
            raise ValueError(f"Invalid character in symbol: {symbol}")

        # If a symbol starting with a number is valid, comment the following check:
        if symbol[0].isdigit():
            raise ValueError(f"Invalid symbol starting with number: {symbol}")

        # Otherwise, its a valid variable/destination
        return types["destination"] if len(self.buffer) == 0 else types["variable"] 

    def tokenize(self, symbol: str) -> Token:
        try: 
            type: int = self.identify(symbol)
        except ValueError as ve:
            raise 

        return Token(symbol, type)

    def readline(self) -> None:
        """
            Tokenizes a line of the input into a list of tokens in the internal buffer.
            Error checking for valid order of tokens is not done. However, valid characters
            should be checked when obtaining the type.

            This method should be called in a try/catch block.
        """
        
        # get leading whitespace out so we can assume we are reading destination immediately
        line = self.file.readline().lstrip() 

        # Tokenize the line
        tokens: list[Token] = []

        symbol: str = ""
        read_cur: bool = False # If we have read in the first character of a symbol

        for char in line:
            if char == '\n':
                # Tokenize what we have, if it exists
                try:
                    if symbol:
                        tokens.append(self.tokenize(symbol))

                    # Then, we tokenize the newline
                    tokens.append(self.tokenize(char))
                except ValueError as ve:
                    raise

            elif not read_cur:
                if char == ' ': # Once we read a full symbol, tokenize it
                    try:
                        tokens.append(self.tokenize(symbol))
                    except ValueError as ve:
                        raise

                    read_cur = True
                    symbol = ""
                else:
                    symbol += char
            else:
                if char != ' ':
                    symbol += char
                    read_cur = False

        # Finally, Reset buffer and index
        self.buffer = tokens
        self.index = 0

    def next_token(self) -> Token:
        if len(self.buffer) == self.index:
            self.readline()
        else:
            self.index += 1

        return self.buffer[self.index]

        
