# Instruction-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — binary operator | `Instruction(0, dest, op1, operator, op2)` | `type == 0`, correct `dest`, `operand1`, `operator`, `operand2` | |
| Construction — unary operator | `Instruction(1, dest, operator=op, operand2=op2)` | `type == 1`, correct `dest`, `operator`, `operand2`, `operand1 == None` | |
| Construction — assignment | `Instruction(2, dest, op1)` | `type == 2`, correct `dest`, `operand1`, `operator == None`, `operand2 == None` | |
| Construction — invalid type | `Instruction(-1, dest)` | `type == -1`, correct `dest`, all other fields `None` | |
| `__str__()` — binary operator | `str(Instruction(0, Token("x",0), Token("a",1), Token("+",3), Token("b",1)))` | `"x = a + b"` | |
| `__str__()` — unary operator | `str(Instruction(1, Token("x",0), operator=Token("-",3), operand2=Token("a",1)))` | `"x = -a"` | |
| `__str__()` — assignment | `str(Instruction(2, Token("x",0), Token("42",2)))` | `"x = 42"` | |
| `get_variables()` — binary, all variables | `Instruction(0, Token("x",0), Token("a",1), Token("+",3), Token("b",1)).get_variables()` | `[Token("x",0), Token("a",1), Token("b",1)]` | |
| `get_variables()` — binary, literal operands | `Instruction(0, Token("x",0), Token("1",2), Token("+",3), Token("2",2)).get_variables()` | `[Token("x",0)]` (only dest) | |
| `get_variables()` — binary, mixed operands | `Instruction(0, Token("x",0), Token("a",1), Token("+",3), Token("2",2)).get_variables()` | `[Token("x",0), Token("a",1)]` | |
| `get_variables()` — unary, variable operand | `Instruction(1, Token("x",0), operator=Token("-",3), operand2=Token("a",1)).get_variables()` | `[Token("x",0), Token("a",1)]` | |
| `get_variables()` — unary, literal operand | `Instruction(1, Token("x",0), operator=Token("-",3), operand2=Token("42",2)).get_variables()` | `[Token("x",0)]` (only dest) | |
| `get_variables()` — assignment, variable operand | `Instruction(2, Token("x",0), Token("a",1)).get_variables()` | `[Token("x",0), Token("a",1)]` | |
| `get_variables()` — assignment, literal operand | `Instruction(2, Token("x",0), Token("42",2)).get_variables()` | `[Token("x",0)]` (only dest) | |