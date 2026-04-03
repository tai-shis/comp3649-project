# Token-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — destination token | `Token("x", 0)` | `value == "x"`, `type == 0` | `value == "x"`, `type == 0` **PASS** |
| Construction — variable token | `Token("a", 1)` | `value == "a"`, `type == 1` | `value == "a"`, `type == 1` **PASS** |
| Construction — literal token | `Token("42", 2)` | `value == "42"`, `type == 2` | `value == "42"`, `type == 2` **PASS** |
| Construction — operator token | `Token("+", 3)` | `value == "+"`, `type == 3` | `value == "+"`, `type == 3` **PASS** |
| Construction — equals token | `Token("=", 4)` | `value == "="`, `type == 4` | `value == "="`, `type == 4` **PASS** |
| Construction — live token | `Token("live:", 5)` | `value == "live:"`, `type == 5` | `value == "live:"`, `type == 5` **PASS** |
| Construction — live symbol token | `Token("a,", 6)` | `value == "a,"`, `type == 6` | `value == "a,"`, `type == 6` **PASS** |
| Construction — newline token | `Token("\n", 7)` | `value == "\n"`, `type == 7` | `value == "\n"`, `type == 7` **PASS** |
| Construction — EOF token | `Token("", -1)` | `value == ""`, `type == -1` | `value == ""`, `type == -1` **PASS** |
| `type_string()` — destination | `Token("x", 0).type_string()` | `"destination"` | `"destination"` **PASS** |
| `type_string()` — variable | `Token("a", 1).type_string()` | `"variable"` | `"variable"` **PASS** |
| `type_string()` — literal | `Token("42", 2).type_string()` | `"literal"` | `"literal"` **PASS** |
| `type_string()` — operator | `Token("+", 3).type_string()` | `"operator"` | `"operator"` **PASS** |
| `type_string()` — equals | `Token("=", 4).type_string()` | `"equals"` | `"equals"` **PASS**|
| `type_string()` — live | `Token("live:", 5).type_string()` | `"live"` | `"live"` **PASS** |
| `type_string()` — live symbol | `Token("a,", 6).type_string()` | `"live_symbol"` | `"live_symbol"` **PASS** |
| `type_string()` — newline | `Token("\n", 7).type_string()` | `"newline"` | `"newline"` **PASS** |
| `type_string()` — EOF | `Token("", -1).type_string()` | `"EOF"` | `"EOF"` **PASS** |
| `__str__()` — destination | `str(Token("x", 0))` | `"'x': destination"` | `"'x': destination"` **PASS** |
| `__str__()` — variable | `str(Token("a", 1))` | `"'a': variable"` | `"'a': variable"` **PASS** |
| `__str__()` — operator | `str(Token("+", 3))` | `"'+': operator"` | `"'+': operator"` **PASS** |
| `__str__()` — EOF | `str(Token("", -1))` | `"'': EOF"` | `"'': EOF"` **PASS** |