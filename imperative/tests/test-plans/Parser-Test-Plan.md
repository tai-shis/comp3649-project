# Parser-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `_validate_instruction()` — valid binary operator | `[dest, equals, variable, operator, variable, newline]` (6 tokens) | Returns `0` | |
| `_validate_instruction()` — valid binary operator with literal | `[dest, equals, literal, operator, literal, newline]` (6 tokens) | Returns `0` | |
| `_validate_instruction()` — valid unary operator | `[dest, equals, operator, variable, newline]` (5 tokens) | Returns `1` | |
| `_validate_instruction()` — valid assignment | `[dest, equals, variable, newline]` (4 tokens) | Returns `2` | |
| `_validate_instruction()` — valid assignment with literal | `[dest, equals, literal, newline]` (4 tokens) | Returns `2` | |
| `_validate_instruction()` — invalid length | `[dest, equals, newline]` (3 tokens) | Returns `-1` | |
| `_validate_instruction()` — wrong token order | `[equals, dest, variable, operator, variable, newline]` (6 tokens) | Returns `-1` | |
| `_validate_instruction()` — missing newline | `[dest, equals, variable, operator, variable]` (5 tokens, no newline) | Returns `-1` | |
| `_parse_instructions()` — single binary instruction | File: `"x = a + b\n"` | Buffer contains 1 `BinaryIns`, `occurred_variables == {"x", "a", "b"}` | |
| `_parse_instructions()` — single unary instruction | File: `"x = - a\n"` | Buffer contains 1 `UnaryIns` | |
| `_parse_instructions()` — single assignment | File: `"x = 42\n"` | Buffer contains 1 `AssignmentIns` | |
| `_parse_instructions()` — multiple instructions | File with 3 instructions | Buffer contains 3 instructions in order | |
| `_parse_instructions()` — stops at live | File: `"x = a + b\nlive:\na,"` | Returns `False`, buffer has 1 instruction, live not yet parsed | |
| `_parse_instructions()` — returns True on EOF | File with only instructions and no live section | Returns `True` | |
| `_parse_instructions()` — invalid instruction raises error | File: `"= x a +\n"` | Raises `ValueError` | |
| `_parse_live()` — single valid live object | File after live: `"a,"`, `a` in `occurred_variables` | Buffer live objects contains `"a"` | |
| `_parse_live()` — multiple valid live objects | `"a, b, c,"`, all in `occurred_variables` | Buffer live objects contains `["a", "b", "c"]` | |
| `_parse_live()` — duplicate live objects dropped | `"a, a, b,"`, all in `occurred_variables` | Buffer live objects contains `["a", "b"]` (no duplicates) | |
| `_parse_live()` — undeclared live object raises error | `"z,"` where `z` not in `occurred_variables` | Raises `ValueError` | |
| `_parse_live()` — invalid token type raises error | Non-live-symbol token after `live:` | Raises `ValueError` | |
| `_parse_live()` — skips newlines | `"live:\na, b,"` | Parses `a` and `b` correctly, newline ignored | |
| `parse()` — full input with instructions and live | `"x = a + b\ny = x\nlive:\na, b,"` | Returns `InstructionBuffer` with 2 instructions, live objects `["a", "b"]`, `occurred_variables == {"x", "a", "b", "y"}` | |
| `parse()` — instructions only, no live section | `"x = a + b\n"` | Returns `InstructionBuffer` with 1 instruction, empty live objects | |
| `parse()` — empty file | Empty file | Returns empty `InstructionBuffer` | |
| `parse()` — occurred variables set on buffer | `"x = a + b\nlive:\na,"` | `instruction_buffer.get_occurred_variables() == {"x", "a", "b"}` | |