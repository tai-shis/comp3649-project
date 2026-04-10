# Parser Test Plan

| Category (Reason) | Test (Input Tokens) | Expected Result | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- |
| `Binary Ops` — Var + Var | `a = b + c` | `BinaryIns(a, b, +, c)` | `BinaryIns(...)` | **PASS** |
| `Binary Ops` — Var * Lit | `t1 = x * 10` | `BinaryIns(t1, x, *, 10)` | `BinaryIns(...)` | **PASS** |
| `Binary Ops` — Lit / Var | `t2 = 10 / y` | `BinaryIns(t2, 10, /, y)` | `BinaryIns(...)` | **PASS** |
| `Binary Ops` — Lit - Lit | `res = 100 - 50` | `BinaryIns(res, 100, -, 50)` | `BinaryIns(...)` | **PASS** |
| `Unary Ops` — Negate Var | `a = - x` | `UnaryIns(a, -, x)` | `UnaryIns(...)` | **PASS** |
| `Unary Ops` — Negate Lit | `b = - 5` | `UnaryIns(b, -, 5)` | `UnaryIns(...)` | **PASS** |
| `Assignment` — Var to Dest | `a = b` | `AssignmentIns(a, b)` | `AssignmentIns(...)` | **PASS** |
| `Assignment` — Lit to Dest | `res = 100` | `AssignmentIns(res, 100)` | `AssignmentIns(...)` | **PASS** |
| `Live Variables` — Single | `Live: res` | `["res"]` | `["res"]` | **PASS** |
| `Live Variables` — Multiple | `Live: a, b` | `["a", "b"]` | `["a", "b"]` | **PASS** |
| `Live Variables` — Massive | `Live: a, b, c, d, e` | `["a", "b", "c", "d", "e"]` | Extracted 5 items | **PASS** |
| `Live Variables` — Empty | `Live:` | `[]` | `[]` | **PASS** |
| `Integration` — Mixed Prog | 2 Instructions + Live line | Correct List & AST | AST Built Correctly | **PASS** |
| `Edge Case` — Empty File | Empty Token List `[]` | Empty Instructions `([], [])`| `([], [])` | **PASS** |
| `Error Handling` — Bad Format| Missing Equals `a b + c` | `Halt: Invalid format` | `Error: Invalid...` | **PASS** |
| `Error Handling` — Missing Dest| Missing Dest `= a + b` | `Halt: Invalid format` | `Error: Invalid...` | **PASS** |
| `Error Handling` — Missing Op | Missing Oper `a = + b` | `Halt: Invalid format` | `Error: Invalid...` | **PASS** |
| `Error Handling` — Bad Order | Tokens after Live line | `Halt: Unexpected tokens` | `Error: Unexpected...` | **PASS** |
| `Error Handling` — Bad Live | `Live: a = b` | `Halt: Invalid tokens...` | `Error: Invalid...` | **PASS** |
| `Error Handling` — Lexical | Illegal Chars `$!@#` | Scanner/Parser Failure | `Error: Invalid...` | **PASS** |