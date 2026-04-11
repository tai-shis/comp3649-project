# ASMGenerator-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — fields initialized | `ASMGenerator(buffer, graph, liveness)` | `generated_asm == []`, `in_register == set()`, `register_colors == graph.colors` | `generated_asm == []`, `in_register == set()`, `register_colors == graph.colors` **PASS** |
| Construction — opcodes initialized | `ASMGenerator(buffer, graph, liveness)` | `opcodes == {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}` | `opcodes == {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}` **PASS** |
| `_get_reg()` — variable assigned to R0 | `Token("a", 1)`, `register_colors = {"a": 0}` | Returns `"R0"` | Returns `"R0"` **PASS**|
| `_get_reg()` — variable assigned to R2 | `Token("b", 1)`, `register_colors = {"b": 2}` | Returns `"R2"` | Returns `"R2"` **PASS** |
| `_get_reg()` — variable not in colors raises error | `Token("z", 1)`, `register_colors = {}` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_get_reg()` — variable with None color raises error | `Token("a", 1)`, `register_colors = {"a": None}` | Raises `ValueError` | Raises `ValueError` **PASS** |
| `_get_op_code()` — addition | `Token("+", 3)` | Returns `"ADD"` | Returns `"ADD"` **PASS** |
| `_get_op_code()` — subtraction | `Token("-", 3)` | Returns `"SUB"` | Returns `"SUB"` **PASS** |
| `_get_op_code()` — multiplication | `Token("*", 3)` | Returns `"MUL"` | Returns `"MUL"` **PASS** |
| `_get_op_code()` — division | `Token("/", 3)` | Returns `"DIV"` | Returns `"DIV"` **PASS** |
| `_load_variable()` — literal returns empty list | `Token("17", 2)`, any `in_register` | Returns `[]` | Returns `[]` **PASS** |
| `_load_variable()` — variable not yet resident emits MOV | `Token("a", 1)`, `register_colors = {"a": 0}`, `in_register = {}` | Returns `[ASMInstruction("MOV", "a", "R0")]`, `"a"` added to `in_register` | Returns `[ASMInstruction("MOV", "a", "R0")]`, `"a"` added to `in_register` **PASS** |
| `_load_variable()` — variable already resident returns empty list | `Token("a", 1)`, `in_register = {"a"}` | Returns `[]` | Returns `[]` **PASS** |
| `_get_operand_str()` — literal returns hash prefixed value | `Token("17", 2)` | Returns `"#17"` | Returns `"#17"` **PASS** |
| `_get_operand_str()` — variable returns register string | `Token("a", 1)`, `register_colors = {"a": 1}` | Returns `"R1"` | Returns `"R1"` **PASS** |
| `_generate_instruction_asm()` — binary, dest == op1 reg, compute in place | `a = a + 1`, `register_colors = {"a": 0}` | `[ASMInstruction("MOV", "a", "R0"), ASMInstruction("ADD", "#1", "R0")]` | `[ASMInstruction("MOV", "a", "R0"), ASMInstruction("ADD", "#1", "R0")]` **PASS** |
| `_generate_instruction_asm()` — binary, dest != op1 reg, MOV before op | `a = b + 1`, `register_colors = {"a": 0, "b": 1}` | Load `b`, `MOV R1,R0`, `ADD #1,R0` | Load `b`, `MOV R1,R0`, `ADD #1,R0` **PASS** |
| `_generate_instruction_asm()` — binary, dest == op2 reg, commutative, swap | `a = b + a`, `register_colors = {"a": 0, "b": 1}` | Load `b`, `ADD R1,R0` (no extra MOV — operands swapped) | Load `b`, `ADD R1,R0` (no extra MOV — operands swapped) **PASS** |
| `_generate_instruction_asm()` — binary, dest == op2 reg, non-commutative, store then reload | `a = 1 - a`, `register_colors = {"a": 0}` | `MOV R0,a`, `MOV #1,R0`, `SUB a,R0` | `MOV R0,a`, `MOV #1,R0`, `SUB a,R0` **PASS** |
| `_generate_instruction_asm()` — binary returns list of ASMInstruction | Any valid binary instruction | Return type is `list[ASMInstruction]` | Return type is `list[ASMInstruction]` **PASS** |
| `_generate_instruction_asm()` — unary negation, dest != source | `x = -a`, `register_colors = {"x": 1, "a": 0}` | Load `a`, `MOV R0,R1`, `MUL #-1,R1` | Load `a`, `MOV R0,R1`, `MUL #-1,R1` **PASS** |
| `_generate_instruction_asm()` — unary negation, dest == source reg | `a = -a`, `register_colors = {"a": 0}` | Load `a`, `MUL #-1,R0` (no MOV needed) | Load `a`, `MUL #-1,R0` (no MOV needed) **PASS** |
| `_generate_instruction_asm()` — unary adds dest to in_register | `a = -b`, `register_colors = {"a": 0, "b": 1}` | `"a"` is in `in_register` after call | `"a"` is in `in_register` after call **PASS** |
| `_generate_instruction_asm()` — assignment, dest != source | `b = a`, `register_colors = {"a": 0, "b": 1}` | Load `a`, `MOV R0,R1` | Load `a`, `MOV R0,R1` **PASS** |
| `_generate_instruction_asm()` — assignment, dest == source reg (no-op) | `a = b`, `register_colors = {"a": 0, "b": 0}` | Load `b` (MOV b,R0), no second MOV since dest == source | Load `b` (MOV b,R0), no second MOV since dest == source **PASS** |
| `_generate_instruction_asm()` — assignment from literal | `a = 17`, `register_colors = {"a": 0}` | `MOV #17,R0` | `MOV #17,R0` **PASS** |
| `_generate_instruction_asm()` — invalid instruction type returns empty | `Instruction(-1, Token("x", 0))` | Returns `[]` | Returns `[]` **PASS** |
| `_generate_instruction_asm()` — store-back triggered when sharing var becomes live | `a = a + 1` where `a` and `t1` share R0, `t1` live on next line | `MOV R0,a` emitted after computation | `MOV R0,a` emitted after computation **PASS** |
| `_generate_instruction_asm()` — store-back not triggered when no sharing var is live | `a = a + 1`, no sharing variables live on next line | No store-back `MOV` emitted | No store-back `MOV` emitted **PASS** |
| `_generate_instruction_asm()` — dest added to in_register after binary | Any valid binary instruction | `instruction.dest.value` in `in_register` after call | `instruction.dest.value` in `in_register` after call **PASS** |
| `_write_live_on_exit()` — stores all live-on-exit variables | Buffer with `live: a`, `register_colors = {"a": 0}` | `generated_asm` ends with `ASMInstruction("MOV", "R0", "a")` | `generated_asm` ends with `ASMInstruction("MOV", "R0", "a")` **PASS** |
| `_write_live_on_exit()` — multiple live-on-exit variables | Buffer with `live: a, b`, `register_colors = {"a": 0, "b": 1}` | `generated_asm` ends with MOV for both `a` and `b` | `generated_asm` ends with MOV for both `a` and `b` **PASS** |
| `_write_live_on_exit()` — no live-on-exit variables | Buffer with empty `live:` | No store instructions added to `generated_asm` | No store instructions added to `generated_asm` **PASS** |
| `generate_assembly()` — single binary instruction | `a = b + c`, all separate registers | `generated_asm` contains correct load and op instructions | `generated_asm` contains correct load and op instructions **PASS** |
| `generate_assembly()` — single unary instruction | `a = -b`, separate registers | `generated_asm` contains load, MOV, MUL #-1 | `generated_asm` contains load, MOV, MUL #-1 **PASS** |
| `generate_assembly()` — single assignment | `a = 17` | `generated_asm` contains `MOV #17,Rn` | `generated_asm` contains `MOV #17,Rn` **PASS** |
| `generate_assembly()` — multiple instructions correct order | 3 instructions | `generated_asm` instructions appear in correct program order | `generated_asm` instructions appear in correct program order **PASS** |
| `generate_assembly()` — returns list of ASMInstruction | Any valid buffer | Return type is `list[ASMInstruction]` | Return type is `list[ASMInstruction]`**PASS** |
| `generate_assembly()` — file created | Call with valid output path | File exists at path after call | File exists at path after call **PASS** |
| `generate_assembly()` — file format correct | Any buffer | Each line formatted as `"OPCODE op1,op2"` | Each line formatted as `"OPCODE op1,op2"` **PASS** |
| `generate_assembly()` — creates missing directories | Path with non-existent directory | Directory created and file written successfully | Directory created and file written successfully **PASS** |
| `generate_assembly()` — chained instructions share register correctly | `a = a + 1`, `a = a - 1` | Second instruction computes in place without reloading `a` | Second instruction computes in place without reloading `a` **PASS** |
| `generate_assembly()` — full pipeline: single_assignment.txt | `a = 17`, `live: a` | `MOV #17,R0` then `MOV R0,a` | `MOV #17,R0` then `MOV R0,a` **PASS** |
| `generate_assembly()` — full pipeline: single_unary.txt | `a = -b`, `live: a` | Load `b`, `MUL #-1`, store `a` | Load `b`, `MUL #-1`, store `a` **PASS** |
| `generate_assembly()` — full pipeline: single_binary.txt | `a = b + c`, `live: a`, separate registers | Load both, ADD, store `a` | Load both, ADD, store `a` **PASS** |
| `generate_assembly()` — full pipeline: assignments.txt | `a=b`, `a=3`, `b=100`, `c=a`, `d=c`, `live: d` | Correct loads, no-ops for same-register assignments, store `d` | Correct loads, no-ops for same-register assignments, store `d` **PASS** |
| `generate_assembly()` — full pipeline: unary_ops.txt | Three chained negations, `live: t2` | Three `MUL #-1` in place, store `t2` | Three `MUL #-1` in place, store `t2` **PASS** |