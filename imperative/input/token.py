class Token:
    types = {
        0: "destination",  # 'd', 't3', 'z', destination (variable)
        1: "variable",     # 'a', 't1', 'b', variables
        2: "literal",      # '1', '23', '415', any integer literal
        3: "operator",     # '+', '-', '*', '/' operators
        4: "equals",
        5: "live",         # 'live:' occurs once
        6: "live_symbol",  # 'a,', 'c,', 'd,', etc... (excluding commas in tokens)
        7: "newline",
        -1: "EOF"
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