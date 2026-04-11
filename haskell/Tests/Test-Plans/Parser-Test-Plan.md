# Parser Test Plan

| Category (Reason) | Test (Input Tokens) | Expected Result | Actual Output |
| :--- | :--- | :--- | :--- |
| binary ops | `a = b + c` | `BinaryIns(a, b, +, c)` | builds binary **PASS** |
| binary ops | `t1 = x * 10` | `BinaryIns(t1, x, *, 10)` | builds binary **PASS** |
| binary ops | `t2 = 10 / y` | `BinaryIns(t2, 10, /, y)` | builds binary **PASS** |
| binary ops | `res = 100 - 50` | `BinaryIns(res, 100, -, 50)` | builds binary **PASS** |
| unary ops | `a = - x` | `UnaryIns(a, -, x)` | builds unary **PASS** |
| unary ops | `b = - 5` | `UnaryIns(b, -, 5)` | builds unary **PASS** |
| assignments | `a = b` | `AssignmentIns(a, b)` | builds assignment **PASS** |
| assignments | `res = 100` | `AssignmentIns(res, 100)` | builds assignment **PASS** |
| live extraction | `Live: res` | `["res"]` | `["res"]` **PASS** |
| live extraction | `Live: a, b` | `["a", "b"]` | `["a", "b"]` **PASS** |
| live extraction | massive list of vars | extracts all 5 items | extracted **PASS** |
| live extraction | empty live line | `[]` | `[]` **PASS** |
| integration | 2 instructions + live line | correct list & AST | ast built perfectly **PASS** |
| edge cases | empty token list | `([], [])`| `([], [])` **PASS** |
| error handling | missing equals (`a b + c`) | halt: invalid format | halts with error **PASS** |
| error handling | missing dest (`= a + b`) | halt: invalid format | halts with error **PASS** |
| error handling | missing operator (`a = + b`) | halt: invalid format | halts with error **PASS** |
| error handling | tokens after live line | halt: unexpected tokens | halts with error **PASS** |
| error handling | bad live syntax (`Live: a = b`) | halt: invalid tokens | halts with error **PASS** |
| error handling | garbage chars (`$!@#`) | halt: scanner failure | halts with error **PASS** |