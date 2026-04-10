# Assembly & Generator Test Plan

*Note: For the logic tests, we mock a register map where a:R0, b:R1, c:R2, d:R3, t1:R0, and t2:R1.*

| Category (Reason) | Test (Input) | Expected Output | Actual Output | Status |
|:------------------|:-------------|:----------------|:--------------|:-------|
| `Show OpCode` — ADD | `show ADD == "ADD"` | `ADD` | `ADD` | **PASS** |
| `Show OpCode` — SUB | `show SUB == "SUB"` | `SUB` | `SUB` | **PASS** |
| `Show OpCode` — MUL | `show MUL == "MUL"` | `MUL` | `MUL` | **PASS** |
| `Show OpCode` — DIV | `show DIV == "DIV"` | `DIV` | `DIV` | **PASS** |
| `Show OpCode` — MOV | `show MOV == "MOV"`| `MOV` | `MOV` | **PASS** |
| `Eq OpCode` — Equal OpCode | `ADD == ADD` | `True` | `True` | **PASS** |
| `Eq OpCode` — Unequal OpCode | `ADD /= MUL` | `True` | `True` | **PASS** |
| `Eq OpCode` — Unequal OpCode | `SUB /= DIV` | `True` | `True` | **PASS** |
| `Show AssemblyInst` - ADD | `show (AssemblyInstruction ADD "#1" "R0")` | `"ADD #1,R0"` | `"ADD #1,R0"` | **PASS** | 
| `Show AssemblyInst` - SUB | `show (AssemblyInstruction SUB "R1" "R2")` | `"SUB R1,R2"` | `"SUB R1,R2"` | **PASS**| 
| `Show AssemblyInst` - MUL | `show (AssemblyInstruction MUL "#10" "R3")` | `"MUL #10,R3"` | `"MUL #10,R3"` | **PASS** | 
| `Show AssemblyInst` - DIV | `show (AssemblyInstruction DIV "R0" "R1")` | `"DIV R0,R1"` | `"DIV R0,R1"` | **PASS** | 
| `Show AssemblyInst` - MOV | `show (AssemblyInstruction MOV "x" "R0")` | `"MOV x,R0"` | `"MOV x,R0"` | **PASS** | 
| `Eq AssemblyInst` — Equal | `AssemblyInstruction MOV "#2" "R0" == AssemblyInstruction MOV "#2" "R0"` | `True` | `True` | **PASS** |
| `Eq AssemblyInst` — Unequal Dest | `AssemblyInstruction MOV "#2" "R0" /= AssemblyInstruction MOV "#2" "R1"` | `True` | `True` | **PASS** |
| `Show Assembly` | `[AssemblyInst MOV "x" "R0", AssemblyInst ADD "#1" "R0"]` | `"MOV x,R0\nADD #1,R0\n"` | `"MOV x,R0\nADD #1,R0\n"` | **PASS** |
| `Liveness` — Entry/Exit Complete | `gen [] ["a","b"] ["c","d"] map` | `[MOV a, R0, MOV b, R1, MOV R2, c, MOV R3, d]` | Matches Expected | **PASS** |
| `Liveness` — Memory Fallback | `gen [] ["x"] ["z"] map` | `[]` (Ignores unregistered vars) | `[]` | **PASS** |
| `Liveness` — Mixed Loading | `gen [] ["a","x"] ["b","y"] map` | `[MOV a, R0, MOV R1, b]` | Matches Expected | **PASS** |
| `Binary ADD` — Var + Var | `d = a + b` | `[MOV R0, R3, ADD R1, R3]` | Matches Expected | **PASS** |
| `Binary ADD` — Commutative | `a = b + a` | `[ADD R1, R0]` (Skips redundant MOV) | Matches Expected | **PASS** |
| `Binary ADD` — Lit + Lit | `a = 5 + 10` | `[MOV #5, R0, ADD #10, R0]` | Matches Expected | **PASS** |
| `Binary SUB` — Var - Var | `c = a - b` | `[MOV R0, R2, SUB R1, R2]` | Matches Expected | **PASS** |
| `Binary SUB` — Var - Lit | `c = a - 5` | `[MOV R0, R2, SUB #5, R2]` | Matches Expected | **PASS** |
| `Binary SUB` — No Commutative | `a = b - a` | `[MOV R1, R0, SUB R0, R0]` | Matches Expected | **PASS** |
| `Binary MUL` — Var * Lit | `c = a * 10` | `[MOV R0, R2, MUL #10, R2]` | Matches Expected | **PASS** |
| `Binary MUL` — Commutative | `a = 10 * a` | `[MUL #10, R0]` (Skips redundant MOV) | Matches Expected | **PASS** |
| `Binary DIV` — Var / Var | `c = a / b` | `[MOV R0, R2, DIV R1, R2]` | Matches Expected | **PASS** |
| `Binary DIV` — Lit / Var | `c = 100 / b` | `[MOV #100, R2, DIV R1, R2]` | Matches Expected | **PASS** |
| `Unary` — Var (Diff Reg) | `b = -a` | `[MOV R0, R1, MUL #-1, R1]` | Matches Expected | **PASS** |
| `Unary` — Var (Same Reg) | `t1 = -a` | `[MUL #-1, R0]` (Skips redundant MOV) | Matches Expected | **PASS** |
| `Unary` — Literal | `a = -5` | `[MOV #5, R0, MUL #-1, R0]` | Matches Expected | **PASS** |
| `Assignment` — Literal | `a = 4` | `[MOV #4, R0]` | Matches Expected | **PASS** |
| `Assignment` — Var (Diff Reg) | `b = a` | `[MOV R0, R1]` | Matches Expected | **PASS** |
| `Assignment` — Redundancy Skip | `t1 = a` | `[]` (Both use R0, skips MOV R0,R0) | `[]` | **PASS** |