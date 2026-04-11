# Assembly Generator Test Plan

*Note: we are using a mocked register map (a:R0,b:R1,c:R2,d:R3,t1:R0,t2:R1) to test assembly generation isolated rather than relying on graph colouring*

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| basic opcodes | `show ADD` | `"ADD"` | `"ADD"` **PASS** |
| basic opcodes | `show SUB` | `"SUB"` | `"SUB"` **PASS** |
| basic opcodes | `show MUL` | `"MUL"` | `"MUL"` **PASS** |
| basic opcodes | `show DIV` | `"DIV"` | `"DIV"` **PASS** |
| basic opcodes | `show MOV` | `"MOV"` | `"MOV"` **PASS** |
| opcode equality | `ADD == ADD` | `True` | `True` **PASS** |
| opcode inequality | `ADD /= MUL` | `True` | `True` **PASS** |
| opcode inequality | `SUB /= DIV` | `True` | `True` **PASS** |
| print instructions | `show (AssemblyInstruction ADD "#1" "R0")` | `"ADD #1,R0"` | `"ADD #1,R0"` **PASS** | 
| print instructions | `show (AssemblyInstruction SUB "R1" "R2")` | `"SUB R1,R2"` | `"SUB R1,R2"` **PASS**| 
| print instructions | `show (AssemblyInstruction MUL "#10" "R3")` | `"MUL #10,R3"` | `"MUL #10,R3"` **PASS** | 
| print instructions | `show (AssemblyInstruction DIV "R0" "R1")` | `"DIV R0,R1"` | `"DIV R0,R1"` **PASS** | 
| print instructions | `show (AssemblyInstruction MOV "x" "R0")` | `"MOV x,R0"` | `"MOV x,R0"` **PASS** | 
| inst equality | `MOV "#2" "R0" == MOV "#2" "R0"` | `True` | `True` **PASS** |
| inst inequality | `MOV "#2" "R0" /= MOV "#2" "R1"` | `True` | `True` **PASS** |
| print whole block | `[MOV "x" "R0", ADD "#1" "R0"]` | `"MOV x,R0\nADD #1,R0\n"` | `"MOV x,R0\nADD #1,R0\n"` **PASS** |
| liveness | `gen [] ["a","b"] ["c","d"] map` | `[MOV a,R0, MOV b,R1, MOV R2,c, MOV R3,d]` | matches expected **PASS** |
| liveness fallback | `gen [] ["x"] ["z"] map` | `[]` (ignores vars not in map) | `[]` **PASS** |
| liveness mixed | `gen [] ["a","x"] ["b","y"] map` | `[MOV a, R0, MOV R1, b]` | matches expected **PASS** |
| binary math | `d = a + b` | `[MOV R0, R3, ADD R1, R3]` | matches expected **PASS** |
| binary opt | `a = b + a` | `[ADD R1, R0]` (skips mov) | matches expected **PASS** |
| literal math | `a = 5 + 10` | `[MOV #5, R0, ADD #10, R0]` | matches expected **PASS** |
| subtraction | `c = a - b` | `[MOV R0, R2, SUB R1, R2]` | matches expected **PASS** |
| subtraction (lit) | `c = a - 5` | `[MOV R0, R2, SUB #5, R2]` | matches expected **PASS** |
| sub order matters | `a = b - a` | `[MOV R1, R0, SUB R0, R0]` | matches expected **PASS** |
| multiplication | `c = a * 10` | `[MOV R0, R2, MUL #10, R2]` | matches expected **PASS** |
| mul opt | `a = 10 * a` | `[MUL #10, R0]` (skips mov) | matches expected **PASS** |
| division | `c = a / b` | `[MOV R0, R2, DIV R1, R2]` | matches expected **PASS** |
| div literals | `c = 100 / b` | `[MOV #100, R2, DIV R1, R2]` | matches expected **PASS** |
| unary minus | `b = -a` | `[MOV R0, R1, MUL #-1, R1]` | matches expected **PASS** |
| unary opt | `t1 = -a` | `[MUL #-1, R0]` (skips mov) | matches expected **PASS** |
| unary literal | `a = -5` | `[MOV #5, R0, MUL #-1, R0]` | matches expected **PASS** |
| assign literal | `a = 4` | `[MOV #4, R0]` | matches expected **PASS** |
| assign var | `b = a` | `[MOV R0, R1]` | matches expected **PASS** |
| redundancy skip | `t1 = a` | `[]` (since both use R0) | `[]` **PASS** |