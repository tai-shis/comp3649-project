# Token-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `Token` construction — basic variable token | `Token "x" Variable` | A `Token` holding string `"x"` and type `Variable` | |
| `Token` construction — literal token | `Token "42" Literal` | A `Token` holding string `"42"` and type `Literal` | |
| `Token` construction — operator token | `Token "+" Operator` | A `Token` holding string `"+"` and type `Operator` | |
| `Token` construction — destination token | `Token "dest" Destination` | A `Token` holding string `"dest"` and type `Destination` | |
| `Token` construction — EOF token | `Token "" EOF` | A `Token` holding string `""` and type `EOF` | |
| `Show` instance for `TokenType` — Variable | `show Variable` | `"Variable"` | |
| `Show` instance for `TokenType` — Operator | `show Operator` | `"Operator"` | |
| `Show` instance for `TokenType` — Newline | `show Newline` | `"Newline"` | |
| `Show` instance for `TokenType` — LiveToken | `show LiveToken` | `"LiveToken"` | |
| `Show` instance for `TokenType` — EOF | `show EOF` | `"EOF"` | |
| `Show` instance for `Token` | `show (Token "x" Variable)` | `"Token \"x\" Variable"` | |
| `Eq` instance for `TokenType` — equal types | `Variable == Variable` | `True` | |
| `Eq` instance for `TokenType` — unequal types | `Variable == Literal` | `False` | |
| `Eq` instance for `Token` — equal tokens | `Token "x" Variable == Token "x" Variable` | `True` | |
| `Eq` instance for `Token` — different string | `Token "x" Variable == Token "y" Variable` | `False` | |
| `Eq` instance for `Token` — different type | `Token "x" Variable == Token "x" Literal` | `False` | |
| `Eq` instance for `Token` — both fields differ | `Token "x" Variable == Token "42" Literal` | `False` | |