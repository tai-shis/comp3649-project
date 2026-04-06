# Instruction-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `createInstruction` — BinaryProps | `createInstruction (dest, op1, operator, op2)` | A `BinaryIns` with correct dest, operands, and operator | A `BinaryIns` with correct dest, operands, and operator **PASS** |
| `createInstruction` — UnaryProps | `createInstruction (dest, operator, op)` | A `UnaryIns` with correct dest, operator, and operand | A `UnaryIns` with correct dest, operator, and operand **PASS** |
| `createInstruction` — AssignmentProps | `createInstruction (dest, op)` | An `AssignmentIns` with correct dest and operand | An `AssignmentIns` with correct dest and operand **PASS** |
| `Show` instance for `BinaryIns` | `show (createInstruction (dest, op1, operator, op2))` | `"Binary Instruction: x : Destination = a : Variable + : Operator b : Variable"` | `"Binary Instruction: x : Destination = a : Variable + : Operator b : Variable"` **PASS** |
| `Show` instance for `UnaryIns` | `show (createInstruction (dest, operator, op))` | `"Unary Instruction: x : Destination = - : Operator a : Variable"` | `"Unary Instruction: x : Destination = - : Operator a : Variable"` **PASS** |
| `Show` instance for `AssignmentIns` | `show (createInstruction (dest, op))` | `"Assignment Instruction: x : Destination = 42 : Literal"` | `"Assignment Instruction: x : Destination = 42 : Literal"` **PASS** |
| `Eq` instance — equal instructions | Two identical `BinaryIns` values | `True` | `True` |
| `Eq` instance — unequal instructions | A `BinaryIns` compared to an `AssignmentIns` | `False` | `False` **PASS** |
| `getDestination` — BinaryIns | `getDestination (createInstruction (dest, op1, operator, op2))` | `dest` token | `dest` token **PASS** |
| `getDestination` — UnaryIns | `getDestination (createInstruction (dest, operator, op))` | `dest` token | `dest` token **PASS** |
| `getDestination` — AssignmentIns | `getDestination (createInstruction (dest, op))` | `dest` token | `dest` token **PASS** |
| `getVariables` — BinaryIns, all variables | `getVariables` on binary with all Variable tokens | `[op1, op2]` (dest is Destination type, not Variable) | `[op1, op2]` (dest is Destination type, not Variable) **PASS** |
| `getVariables` — BinaryIns, no variables | `getVariables` on binary with Literal operands | `[]` | `[]` **PASS** |
| `getVariables` — BinaryIns, mixed tokens | `getVariables` on binary with one Variable and one Literal operand | `[op1]` | `[op1]` **PASS** |
| `getVariables` — UnaryIns, variable operand | `getVariables` on unary with Variable operand | `[op]` | `[op]` **PASS** |
| `getVariables` — UnaryIns, no variables | `getVariables` on unary with Literal operand | `[]` | `[]` **PASS** |
| `getVariables` — AssignmentIns, variable operand | `getVariables` on assignment with Variable operand | `[op]` | `[op]` **PASS** |
| `getVariables` — AssignmentIns, no variables | `getVariables` on assignment with Literal operand | `[]` | `[]` **PASS** |
| `emptyInstructions` — empty instructions list | `getInstructions emptyInstructions` | `[]` | `[]` **PASS** |
| `emptyInstructions` — empty live variables list | `getLiveVariables emptyInstructions` | `[]` | `[]` **PASS** |
| `fromArraysInstructions` — stores instructions | `getInstructions (fromArraysInstructions [instr] [])` | `[instr]` | `[instr]` **PASS** |
| `fromArraysInstructions` — stores live variables | `getLiveVariables (fromArraysInstructions [] ["a", "b"])` | `["a", "b"]` | `["a", "b"]` **PASS** |
| `fromArraysInstructions` — stores both | `fromArraysInstructions [instr] ["a"]` | `getInstructions` returns `[instr]`, `getLiveVariables` returns `["a"]` | `getInstructions` returns `[instr]`, `getLiveVariables` returns `["a"]` **PASS** |
| `getInstructions` — empty | `getInstructions emptyInstructions` | `[]` | `[]` **PASS** |
| `getInstructions` — populated | `getInstructions (fromArraysInstructions [instr1, instr2] [])` | `[instr1, instr2]` | `[instr1, instr2]` **PASS** |
| `getLiveVariables` — empty | `getLiveVariables emptyInstructions` | `[]` | `[]` **PASS** |
| `getLiveVariables` — populated | `getLiveVariables (fromArraysInstructions [] ["a", "b"])` | `["a", "b"]` | `["a", "b"]` **PASS** |
| `showInstructions` — empty list | `showInstructions []` | `"Instructions: \n"` | `"Instructions: \n"` **PASS** |
| `showInstructions` — single instruction | `showInstructions [assignIns]` | `"Instructions: \nAssignment Instruction: x : Destination = 42 : Literal\n"` | `"Instructions: \nAssignment Instruction: x : Destination = 42 : Literal\n"` **PASS** |
| `showInstructions` — multiple instructions | `showInstructions [assignIns1, assignIns2]` | Both instructions on separate lines prefixed with `"Instructions: \n"` | Both instructions on separate lines prefixed with `"Instructions: \n"` **PASS** |
| `showLiveVars` — empty list | `showLiveVars []` | `"Live: "` | `"Live: "` **PASS** |
| `showLiveVars` — single variable | `showLiveVars ["x"]` | `"Live: x"` | `"Live: x"` **PASS** |
| `showLiveVars` — multiple variables | `showLiveVars ["x", "y"]` | `"Live: x, y"` | `"Live: x, y"` **PASS** |
| `Show` instance for `Instructions` | `show (fromArraysInstructions [assignIns] ["x"])` | `showInstructions [assignIns] ++ showLiveVars ["x"]` | `showInstructions [assignIns] ++ showLiveVars ["x"]` **PASS** |