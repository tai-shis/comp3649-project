# Parser-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `_validate_instruction()` — valid binary operator with variables | `[Token("x",0), Token("=",4), Token("a",1), Token("+",3), Token("b",1), Token("\n",7)]` | `0` | `0` **PASS** |
| `_validate_instruction()` — valid binary operator with literals | `[Token("x",0), Token("=",4), Token("1",2), Token("+",3), Token("2",2), Token("\n",7)]` | `0` | `0` **PASS** |
| `_validate_instruction()` — valid unary operator | `[Token("x",0), Token("=",4), Token("-",3), Token("a",1), Token("\n",7)]` | `1` | `1` **PASS** |
| `_validate_instruction()` — valid assignment with variable | `[Token("x",0), Token("=",4), Token("a",1), Token("\n",7)]` | `2` | `2` **PASS** |
| `_validate_instruction()` — valid assignment with literal | `[Token("x",0), Token("=",4), Token("29",2), Token("\n",7)]` | `2` | `2` **PASS** |
| `_validate_instruction()` — invalid length | `[Token("x",0), Token("=",4), Token("\n",7)]` | `-1` | `-1` **PASS** |
| `_validate_instruction()` — wrong token order | `[Token("=",4), Token("x",0), Token("a",1), Token("+",3), Token("b",1), Token("\n",7)]` | `-1` | `-1` **PASS** |
| `_validate_instruction()` — missing newline | `[Token("x",0), Token("=",4), Token("a",1), Token("+",3), Token("b",1)]` | `-1` | `-1` **PASS** |
| `_parse_instructions()` — single binary instruction | `StringIO("x = a + b\n")` | Buffer contains 1 `BinaryIns`, `occurred_variables == {"x", "a", "b"}`, `instructions[0] == "x = a + b"` | `occurred_variables == {"x", "a", "b"}`; `instructions[0] == "x = a + b"` **PASS** |
| `_parse_instructions()` — single unary instruction | `StringIO("x = - a\n")` | Buffer contains 1 `UnaryIns`, `occurred_variables == {"x", "a"}`, `instructions[0] == "x = -a"` | `occurred_variables == {"x", "a"}; instructions[0] == "x = -a"` **PASS** |
| `_parse_instructions()` — single assignment | `StringIO("x = 32\n")` | Buffer contains 1 `AssignmentIns`, `occurred_variables == {"x"}`; `instructions[0] == "x = 32"` | `occurred_variables == {"x"}`; `instructions[0] == "x = 32"` **PASS** |
| `_parse_instructions()` — multiple instructions | `StringIO("x = a + b\ny = x\nz = y\n")` | Buffer contains 3 instructions in order, `occurred_variables == {"x", "a", "b", "y", "z"}`, `instructions[0] == "x = a + b", instructions[1] == "y = x", instructions[2] == "z = y` | `occurred_variables == {"x", "a", "b", "y", "z"}`, `instructions[0] == "x = a + b", instructions[1] == "y = x", instructions[2] == "z = y` **PASS** |
| `_parse_instructions()` — stops at live | `StringIO("x = a + b\nlive:\na,")` | Returns `False`, buffer has 1 instruction, `instructions[0] == "x = a + b"` | Return `False`; `instructions[0] == "x = a + b"` **PASS** |
| `_parse_instructions()` — returns True on EOF | `StringIO("x = a + b\n")` | Returns `True` | Returns `True` **PASS** |
| `_parse_instructions()` — invalid instruction raises error | `StringIO("= x a +\n")` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_parse_live()` — single valid live object | `StringIO("x = a\nlive:\na,")` | Buffer live objects contains `["a"]` | Buffer live objects contains `["a"]` **PASS** |
| `_parse_live()` — multiple valid live objects | `StringIO("x = a + b\nb = c + 1\nlive:\na, b, c,")` | Buffer live objects contains `["a", "b", "c"]` | Buffer live objects contains `["a", "b", "c"]` **PASS** |
| `_parse_live()` — duplicate live objects dropped | `StringIO("x = a + b\nlive:\na, a, b,")`| Buffer live objects contains `["a", "b"]` | Buffer live objects contains `["a", "b"]` **PASS** |
| `_parse_live()` — undeclared live object raises error | `StringIO("x = a\nlive:\nz,")`| Raises `ValueError` | Raises `ValueError` **PASS** |
| `_parse_live()` — invalid token type raises error | `StringIO("x = a\nlive:\n=")`, `occurred_variables = {"a"}` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_parse_live()` — skips newlines | `StringIO("x = a + b\nlive:\na,\nb,")` | Buffer live objects contains `["a", "b"]` | Buffer live objects contains `["a", "b"]` **PASS** |
| `parse()` — full input with instructions and live | `StringIO("x = a + b\ny = x\nlive:\na, b,")` | `InstructionBuffer` with 2 instructions: `instructions[0] = "x = a + b", instructions[1] == y = x`, live objects `["a", "b"]`, `occurred_variables == {"x", "a", "b", "y"}` | `instructions[0] = "x = a + b", instructions[1] == y = x`, live objects `["a", "b"]`, `occurred_variables == {"x", "a", "b", "y"}` **PASS**|
| `parse()` — instructions only, no live section | `StringIO("x = a + b\n")` | `InstructionBuffer` with 1 instruction: `instructions[0] == x = a + b`, empty live objects | `instructions[0] == x = a + b`; live objects = `[]` **PASS** |
| `parse()` — empty file | `StringIO("")` | `len(buffer.instructions) == 0` | `len(buffer.instructions) == 0` **PASS** |
| `parse()` — occurred variables set on buffer | `StringIO("x = a + b\nlive:\na,")` | `instruction_buffer.get_occurred_variables() == {"x", "a", "b"}` | `instruction_buffer.get_occurred_variables() == {"x", "a", "b"}`  **PASS** |