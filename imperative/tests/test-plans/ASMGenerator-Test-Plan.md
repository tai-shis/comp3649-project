# ASMGenerator-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — fields initialized | `ASMGenerator(buffer, graph)` | `generated_asm == []`, `register_colors == graph.colors`, `buffer == instruction_buffer` | |
| Construction — opcodes initialized | `ASMGenerator(buffer, graph)` | `opcodes == {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}` | |
| `_get_reg_or_value()` — literal token | `Token("42", 2)` with any register colors | Returns `"#42"` | |
| `_get_reg_or_value()` — variable assigned to R0 | `Token("a", 1)`, `register_colors = {"a": 0}` | Returns `"R0"` | |
| `_get_reg_or_value()` — variable assigned to R2 | `Token("b", 1)`, `register_colors = {"b": 2}` | Returns `"R2"` | |
| `_get_reg_or_value()` — variable with no register raises error | `Token("z", 1)`, `register_colors = {}` | Raises `ValueError` | |
| `_get_reg_or_value()` — variable with None color | `Token("a", 1)`, `register_colors = {"a": None}` | Returns `"a"` (fallback to value) | |
| `_get_op_code()` — addition | `Token("+", 3)` | Returns `"ADD"` | |
| `_get_op_code()` — subtraction | `Token("-", 3)` | Returns `"SUB"` | |
| `_get_op_code()` — multiplication | `Token("*", 3)` | Returns `"MUL"` | |
| `_get_op_code()` — division | `Token("/", 3)` | Returns `"DIV"` | |
| `_generate_instruction_asm()` — binary operator | `Instruction(0, Token("x",0), Token("a",1), Token("+",3), Token("b",1))`, `register_colors = {"x": 0, "a": 1, "b": 2}` | Returns `[ASMInstruction("MOV", "a", "R0"), ASMInstruction("ADD", "b", "R0")]` | |
| `_generate_instruction_asm()` — binary with literal operand | `Instruction(0, Token("x",0), Token("1",2), Token("+",3), Token("2",2))`, `register_colors = {"x": 0}` | Returns `[ASMInstruction("MOV", "1", "R0"), ASMInstruction("ADD", "#2", "R0")]` | |
| `_generate_instruction_asm()` — unary negation | `Instruction(1, Token("x",0), operator=Token("-",3), operand2=Token("a",1))`, `register_colors = {"x": 1, "a": 0}` | Returns `[ASMInstruction("MOV", "a", "R1"), ASMInstruction("MUL", "#-1", "R1")]` | |
| `_generate_instruction_asm()` — assignment from variable | `Instruction(2, Token("x",0), Token("a",1))`, `register_colors = {"x": 1, "a": 0}` | Returns `[ASMInstruction("MOV", "R0", "R1")]` | |
| `_generate_instruction_asm()` — assignment from literal | `Instruction(2, Token("x",0), Token("42",2))`, `register_colors = {"x": 0}` | Returns `[ASMInstruction("MOV", "#42", "R0")]` | |
| `_generate_instruction_asm()` — invalid instruction type | `Instruction(-1, Token("x",0))` | Returns `[]` | |
| `_generate_instruction_asm()` — returns list of ASMInstruction | Any valid instruction | Return type is `list[ASMInstruction]` | |
| `generate_assembly()` — single binary instruction | Buffer with `"x = a + b\n"`, colors assigned | `generated_asm` contains 2 `ASMInstruction` objects (MOV + op), file written | |
| `generate_assembly()` — single assignment | Buffer with `"x = a\n"`, colors assigned | `generated_asm` contains 1 `ASMInstruction` (MOV), file written | |
| `generate_assembly()` — multiple instructions | Buffer with 3 instructions | `generated_asm` contains the correct total number of `ASMInstruction` objects in order | |
| `generate_assembly()` — returns list | Any buffer | Return type is `list[ASMInstruction]` | |
| `_output_to_file()` — file created | Call `generate_assembly("output/test.asm")` | File exists at `"output/test.asm"` after the call | |
| `_output_to_file()` — correct file format | Buffer with `"x = a + b\n"`, colors assigned | Each line in file formatted as `"OPCODE op1,op2"` | |
| `_output_to_file()` — creates missing directories | Path with non-existent directory `"output/subdir/test.asm"` | Directory created and file written successfully | |
| `_output_to_file()` — correct number of lines | Buffer with 2 instructions generating 4 ASM instructions | Output file contains exactly 4 lines | |