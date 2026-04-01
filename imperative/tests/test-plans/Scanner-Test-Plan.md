# Scanner-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `next_token()` — destination token | File containing `"x = a + b\n"` | First token: `value == "x"`, `type == 0` (destination) | |
| `next_token()` — equals token | File containing `"x = a + b\n"` | Second token: `value == "="`, `type == 4` (equals) | |
| `next_token()` — variable token | File containing `"x = a + b\n"` | Third token: `value == "a"`, `type == 1` (variable) | |
| `next_token()` — operator token | File containing `"x = a + b\n"` | Fourth token: `value == "+"`, `type == 3` (operator) | |
| `next_token()` — newline token | File containing `"x = a + b\n"` | Sixth token: `value == "\n"`, `type == 7` (newline) | |
| `next_token()` — EOF token | Empty file | `value == ""`, `type == -1` (EOF) | |
| `next_token()` — EOF after last line | File with one instruction and no trailing newline | Returns EOF token after all tokens consumed | |
| `next_token()` — live token | File containing `"live:"` | Token: `value == "live:"`, `type == 5` | |
| `next_token()` — live symbol token | File containing `"live:\na,"` | Token after live: `value == "a"`, `type == 6` | |
| `next_token()` — literal token | File containing `"x = 42\n"` | Third token: `value == "42"`, `type == 2` (literal) | |
| `_identify()` — invalid character in symbol | `"x$"` | Raises `ValueError` | |
| `_identify()` — symbol starting with digit | `"1abc"` | Raises `ValueError` | |
| `_identify()` — operator mixed with symbol | `"a+b"` | Raises `ValueError` | |
| `_tokenize_line()` — binary operator line | `"x = a + b\n"` | Buffer contains 6 tokens: destination, equals, variable, operator, variable, newline | |
| `_tokenize_line()` — unary operator line | `"x = - a\n"` | Buffer contains 5 tokens: destination, equals, operator, variable, newline | |
| `_tokenize_line()` — assignment line | `"x = 42\n"` | Buffer contains 4 tokens: destination, equals, literal, newline | |
| `_tokenize_line()` — live line | `"live:\n"` | Buffer contains 2 tokens: live, newline | |
| `_tokenize_line()` — live symbols | `"a, b, c,"` | Buffer contains 3 live symbol tokens | |
| `_tokenize_line()` — leading whitespace stripped | `"   x = a + b\n"` | Same 6 tokens as without leading whitespace | |
| `_readline()` — returns False on valid line | File with `"x = a + b\n"` | Returns `False`, buffer populated with 6 tokens | |
| `_readline()` — returns True on empty file | Empty file | Returns `True` | |