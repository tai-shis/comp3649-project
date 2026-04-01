# Token-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — destination token | `Token("x", 0)` | `value == "x"`, `type == 0` | |
| Construction — variable token | `Token("a", 1)` | `value == "a"`, `type == 1` | |
| Construction — literal token | `Token("42", 2)` | `value == "42"`, `type == 2` | |
| Construction — operator token | `Token("+", 3)` | `value == "+"`, `type == 3` | |
| Construction — equals token | `Token("=", 4)` | `value == "="`, `type == 4` | |
| Construction — live token | `Token("live:", 5)` | `value == "live:"`, `type == 5` | |
| Construction — live symbol token | `Token("a,", 6)` | `value == "a,"`, `type == 6` | |
| Construction — newline token | `Token("\n", 7)` | `value == "\n"`, `type == 7` | |
| Construction — EOF token | `Token("", -1)` | `value == ""`, `type == -1` | |
| `type_string()` — destination | `Token("x", 0).type_string()` | `"destination"` | |
| `type_string()` — variable | `Token("a", 1).type_string()` | `"variable"` | |
| `type_string()` — literal | `Token("42", 2).type_string()` | `"literal"` | |
| `type_string()` — operator | `Token("+", 3).type_string()` | `"operator"` | |
| `type_string()` — equals | `Token("=", 4).type_string()` | `"equals"` | |
| `type_string()` — live | `Token("live:", 5).type_string()` | `"live"` | |
| `type_string()` — live symbol | `Token("a,", 6).type_string()` | `"live_symbol"` | |
| `type_string()` — newline | `Token("\n", 7).type_string()` | `"newline"` | |
| `type_string()` — EOF | `Token("", -1).type_string()` | `"EOF"` | |
| `__str__()` — destination | `str(Token("x", 0))` | `"'x': destination"` | |
| `__str__()` — variable | `str(Token("a", 1))` | `"'a': variable"` | |
| `__str__()` — operator | `str(Token("+", 3))` | `"'+': operator"` | |
| `__str__()` — EOF | `str(Token("", -1))` | `"'': EOF"` | |