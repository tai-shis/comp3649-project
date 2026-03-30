# Token-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `Token` construction — basic variable token | `Token "x" Variable` | A `Token` holding string `"x"` and type `Variable` | A `Token` holding string `"x"` and type `Variable` **PASS** |
| `Token` construction — literal token | `Token "42" Literal` | A `Token` holding string `"42"` and type `Literal` | A `Token` holding string `"42"` and type `Literal` **PASS** |
| `Token` construction — operator token | `Token "+" Operator` | A `Token` holding string `"+"` and type `Operator` | A `Token` holding string `"+"` and type `Operator` **PASS** |
| `Token` construction — destination token | `Token "dest" Destination` | A `Token` holding string `"dest"` and type `Destination` | A `Token` holding string `"dest"` and type `Destination`  **PASS** |
| `Token` construction — EOF token | `Token "" EOF` | A `Token` holding string `""` and type `EOF` | A `Token` holding string `""` and type `EOF` **PASS** |
| `Show` instance for `TokenType` — Variable | `show Variable` | `"Variable"` | `"Variable"` **PASS** |
| `Show` instance for `TokenType` — Operator | `show Operator` | `"Operator"` | `"Operator"` **PASS** |
| `Show` instance for `TokenType` — Newline | `show Newline` | `"Newline"` | `"Newline"` **PASS** |
| `Show` instance for `TokenType` — LiveToken | `show LiveToken` | `"LiveToken"` | `"LiveToken"` **PASS** |
| `Show` instance for `TokenType` — EOF | `show EOF` | `"EOF"` | `"EOF"`  **PASS** |
| `Show` instance for `Token` | `show (Token "x" Variable)` | `"Token \"x\" Variable"` | `"Token \"x\" Variable"` **PASS** |
| `Eq` instance for `TokenType` — equal types | `Variable == Variable` | `True` | `True` **PASS** |
| `Eq` instance for `TokenType` — unequal types | `Variable == Literal` | `False` | `False` **PASS** |
| `Eq` instance for `Token` — equal tokens | `Token "x" Variable == Token "x" Variable` | `True` | `True` **PASS** |
| `Eq` instance for `Token` — different string | `Token "x" Variable == Token "y" Variable` | `False` | `False` **PASS** |
| `Eq` instance for `Token` — different type | `Token "x" Variable == Token "x" Literal` | `False` | `False` **PASS** |
| `Eq` instance for `Token` — both fields differ | `Token "x" Variable == Token "42" Literal` | `False` | `False` **PASS** |