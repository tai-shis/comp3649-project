# ASMInstruction-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — MOV instruction | `ASMInstruction("MOV", "R0", "R1")` | `op_code == "MOV"`, `op1 == "R0"`, `op2 == "R1"` | `op_code == "MOV"`, `op1 == "R0"`, `op2 == "R1"` **PASS** |
| Construction — ADD instruction | `ASMInstruction("ADD", "#1", "R0")` | `op_code == "ADD"`, `op1 == "#1"`, `op2 == "R0"` | `op_code == "ADD"`, `op1 == "#1"`, `op2 == "R0"` **PASS** |
| Construction — SUB instruction | `ASMInstruction("SUB", "R1", "R0")` | `op_code == "SUB"`, `op1 == "R1"`, `op2 == "R0"` | `op_code == "SUB"`, `op1 == "R1"`, `op2 == "R0"` **PASS** |
| Construction — MUL instruction | `ASMInstruction("MUL", "#-1", "R0")` | `op_code == "MUL"`, `op1 == "#-1"`, `op2 == "R0"` | `op_code == "MUL"`, `op1 == "#-1"`, `op2 == "R0"` **PASS** |
| Construction — DIV instruction | `ASMInstruction("DIV", "R2", "R0")` | `op_code == "DIV"`, `op1 == "R2"`, `op2 == "R0"` | `op_code == "DIV"`, `op1 == "R2"`, `op2 == "R0"` **PASS** |
| Construction — literal operand | `ASMInstruction("MOV", "#29", "R0")` | `op1 == "#42"` | `op1 == "#29"` **PASS** |