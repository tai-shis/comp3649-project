# Scanner-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `next_token()` — destination token | File containing `"x = a + b\n"` | First token: `value == "x"`, `type == 0` (destination) | First token: `value == "x"`, `type == 0` (destination) **PASS** |
| `next_token()` — equals token | File containing `"x = a + b\n"` | Second token: `value == "="`, `type == 4` (equals) | Second token: `value == "="`, `type == 4` (equals) **PASS** |
| `next_token()` — variable token | File containing `"x = a + b\n"` | Third token: `value == "a"`, `type == 1` (variable) | Third token: `value == "a"`, `type == 1` (variable) **PASS** |
| `next_token()` — operator token | File containing `"x = a + b\n"` | Fourth token: `value == "+"`, `type == 3` (operator) | Fourth token: `value == "+"`, `type == 3` (operator) **PASS** |
| `next_token()` — newline token | File containing `"x = a + b\n"` | Sixth token: `value == "\n"`, `type == 7` (newline) | Sixth token: `value == "\n"`, `type == 7` (newline) **PASS** |
| `next_token()` — EOF token | Empty file | `value == ""`, `type == -1` (EOF) | `value == ""`, `type == -1` (EOF) **PASS** |
| `next_token()` — EOF after last line | File with one instruction and no trailing newline | Returns EOF token after all tokens consumed | Returns EOF token after all tokens consumed **PASS** |
| `next_token()` — live token | File containing `"live:"` | Token: `value == "live:"`, `type == 5` | Token: `value == "live:"`, `type == 5` **PASS** |
| `next_token()` — live symbol token | File containing `"live:\na,"` | Token after live: `value == "a"`, `type == 6` | Token after live: `value == "a"`, `type == 6` **PASS** |
| `next_token()` — literal token | File containing `"x = 42\n"` | Third token: `value == "42"`, `type == 2` (literal) | Third token: `value == "42"`, `type == 2` (literal) **PASS** |
| `_identify()` — invalid character in symbol | `"x$"` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_identify()` — symbol starting with digit | `"1abc"` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_identify()` — operator mixed with symbol | `"a+b"` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_tokenize_line()` — binary operator line | `"x = a + b\n"` | Buffer contains 6 tokens: destination, equals, variable, operator, variable, newline | Buffer contains 6 tokens: destination, equals, variable, operator, variable, newline **PASS** |
| `_tokenize_line()` — unary operator line | `"x = - a\n"` | Buffer contains 5 tokens: destination, equals, operator, variable, newline | Buffer contains 5 tokens: destination, equals, operator, variable, newline **PASS** |
| `_tokenize_line()` — assignment line | `"x = 42\n"` | Buffer contains 4 tokens: destination, equals, literal, newline | Buffer contains 4 tokens: destination, equals, literal, newline **PASS** |
| `_tokenize_line()` — live line | `"live:\n"` | Buffer contains 2 tokens: live, newline | Buffer contains 2 tokens: live, newline **PASS** |
| `_tokenize_line()` — live symbols | `"live: a, b, c"` | Buffer contains 3 live symbol tokens | Buffer contains 3 live symbol tokens **PASS** |
| `_readline()` — returns False on valid line | File with `"x = a + b\n"` | Returns `False`, buffer populated with 6 tokens | Returns `False`, buffer populated with 6 tokens **PASS** |
| `_readline()` — returns True on empty file | Empty file | Returns `True` | Returns `True` **PASS** |