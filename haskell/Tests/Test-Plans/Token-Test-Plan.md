# Token-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `createToken` — getValue returns correct value | `getValue (createToken "x" Destination)` | `"x"` | `"x"` **PASS** |
| `createToken` — getType returns correct type | `getType (createToken "x" Destination)` | `Destination` | `Destination` **PASS** |
| `createToken` — Variable type | `getType (createToken "a" Variable)` | `Variable` | `Variable` **PASS** |
| `createToken` — Literal type | `getType (createToken "42" Literal)` | `Literal` | `Literal` **PASS** |
| `createToken` — Operator type | `getType (createToken "+" Operator)` | `Operator` | `Operator` **PASS** |
| `createToken` — Equals type | `getType (createToken "=" Equals)` | `Equals` | `Equals` **PASS** |
| `createToken` — Live type | `getType (createToken "live:" Live)` | `Live` | `Live` **PASS** |
| `createToken` — LiveSymbol type | `getType (createToken "a," LiveSymbol)` | `LiveSymbol` | `LiveSymbol` **PASS** |
| `createToken` — Newline type | `getType (createToken "\n" Newline)` | `Newline` | `Newline` **PASS** |
| `createToken` — EOF type | `getType (createToken "" EOF)` | `EOF` | `EOF` **PASS** |
| `getValue` — variable name | `getValue (createToken "abc" Variable)` | `"abc"` | `"abc"`  **PASS**|
| `getValue` — empty string | `getValue (createToken "" EOF)` | `""` | `""` **PASS** |
| `getValue` — operator symbol | `getValue (createToken "+" Operator)` | `"+"` | `"+"` **PASS** |
| `getType` — Destination | `getType (createToken "x" Destination)` | `Destination` | `Destination` **PASS** |
| `getType` — Literal | `getType (createToken "99" Literal)` | `Literal` | `Literal` **PASS** |
| `getType` — EOF | `getType (createToken "" EOF)` | `EOF` | `EOF` **PASS** |
| `Show` instance for `TokenType` — Destination | `show Destination` | `"Destination"` | `"Destination"` **PASS** |
| `Show` instance for `TokenType` — Variable | `show Variable` | `"Variable"` | `"Variable"` **PASS** |
| `Show` instance for `TokenType` — Literal | `show Literal` | `"Literal"` | `"Literal"` **PASS** |
| `Show` instance for `TokenType` — Operator | `show Operator` | `"Operator"` | `"Operator"` **PASS** |
| `Show` instance for `TokenType` — Equals | `show Equals` | `"Equals"` | `"Equals"` **PASS** |
| `Show` instance for `TokenType` — Live | `show Live` | `"Live"` | `"Live"` **PASS** |
| `Show` instance for `TokenType` — LiveSymbol | `show LiveSymbol` | `"LiveSymbol"` | `"LiveSymbol"` **PASS** |
| `Show` instance for `TokenType` — Newline | `show Newline` | `"Newline"` | `"Newline"` **PASS** |
| `Show` instance for `TokenType` — EOF | `show EOF` | `"EOF"` | `"EOF"` **PASS** |
| `Show` instance for `Token` — variable | `show (createToken "x" Variable)` | `"x : Variable"` | `"x : Variable"` **PASS** |
| `Show` instance for `Token` — literal | `show (createToken "42" Literal)` | `"42 : Literal"` | `"42 : Literal"` **PASS** |
| `Show` instance for `Token` — operator | `show (createToken "+" Operator)` | `"+ : Operator"` | `"+ : Operator"` **PASS** |
| `Show` instance for `Token` — EOF | `show (createToken "" EOF)` | `" : EOF"` | `" : EOF"` **PASS** |
| `Eq` instance for `Token` — equal tokens | `createToken "x" Variable == createToken "x" Variable` | `True` | `True` **PASS** |
| `Eq` instance for `Token` — different value | `createToken "x" Variable /= createToken "y" Variable` | `True` | `True` **PASS** |
| `Eq` instance for `Token` — different type | `createToken "x" Variable /= createToken "x" Literal` | `True` | `True` **PASS** |
| `Eq` instance for `Token` — both fields differ | `createToken "x" Variable /= createToken "42" Literal` | `True` | `True` **PASS** |
| `Eq` instance for `TokenType` — equal | `Variable == Variable` | `True` | `True` **PASS** |
| `Eq` instance for `TokenType` — unequal | `Variable /= Literal` | `True` | `True` **PASS** |