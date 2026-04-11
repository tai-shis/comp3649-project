# Assembly Test Plan
| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `Show OpCode` — ADD | `show ADD == "ADD"` | `ADD` | `ADD` **PASS** |
| `Show OpCode` — SUB | `show SUB == "SUB"` | `SUB` | `SUB` **PASS** |
| `Show OpCode` — MUL | `show MUL == "MUL"` | `MUL` | `MUL` **PASS** |
| `Show OpCode` — DIV | `show DIV == "DIV"` | `DIV` | `DIV` **PASS** |
| `Show OpCode` — MOV | `show MOV == "MOV"`| `MOV` | `MOV` **PASS** |
| `Eq OpCode` — Equal OpCode | `ADD == ADD` | `True` | `True` **PASS** |
| `Eq OpCode` — Unequal OpCode | `ADD /= MUL` | `True` | `True` **PASS** |
| `Show AssemblyInstruction` - ADD instruction | `show AssemblyInstruction ADD "#1" "R0" | `"ADD #1,R0"` | `"ADD #1,R0"` **PASS** | 
| `Show AssemblyInstruction` - SUB instruction | `show AssemblyInstruction SUB "#1" "R0" | `"SUB #1,R0"` | `"SUB #1,R0"`  **PASS**| 
| `Show AssemblyInstruction` - MUL instruction | `show AssemblyInstruction MUL "#2" "R0" | `"MUL #2,R0"` | `"MUL #2,R0"` **PASS** | 
| `Show AssemblyInstruction` - DIV instruction | `show AssemblyInstruction DIV "#2" "R0" | `"DIV #2,R0"` | `"DIV #2,R0"` **PASS** | 
| `Show AssemblyInstruction` - MOV instruction | `show AssemblyInstruction MOV "#1" "R0" | `"MOV #1,R0"` | `"MOV #1,R0"` **PASS** | 
| `Eq AssemblyInstruction` — Equal instruction | `AssemblyInstruction MOV "#2" "R0" == AssemblyInstruction MOV "#2" "R0"` | `True` | `True` **PASS** |
| `Eq AssemblyInstruction` — Unequal instruction | `AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction ADD "x" "R0"` | `True` | `True` **PASS** |
| `Show Assembly` | `[AssemblyInstruction MOV "x" "R0", AssemblyInstruction ADD "#1" "R0"]` | `"Assembly Instructions: \nMOV x,R0\nADD #1,R0\n"` | `"Assembly Instructions: \nMOV x,R0\nADD #1,R0\n"` **PASS** |
