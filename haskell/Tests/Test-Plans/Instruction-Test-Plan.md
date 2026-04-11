# Instruction Test Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| creation | `createInstruction` binary | `BinaryIns` with correct parts | as expected **PASS** |
| creation | `createInstruction` unary | `UnaryIns` with correct parts | as expected **PASS** |
| creation | `createInstruction` assignment | `AssignmentIns` with correct parts | as expected **PASS** |
| printing | `show binaryIns` | `"Binary Instruction: x : Destination = a : Variable + : Operator b : Variable"` | matches expected **PASS** |
| printing | `show unaryIns` | `"Unary Instruction: x : Destination = - : Operator a : Variable"` | matches expected **PASS** |
| printing | `show assignIns` | `"Assignment Instruction: x : Destination = 42 : Literal"` | matches expected **PASS** |
| equality | two identical `BinaryIns` | `True` | `True` **PASS** |
| inequality | `BinaryIns` vs `AssignmentIns` | `False` | `False` **PASS** |
| get dest | `getDestination` on binary | returns the `dest` token | `dest` token **PASS** |
| get dest | `getDestination` on unary | returns the `dest` token | `dest` token **PASS** |
| get dest | `getDestination` on assignment | returns the `dest` token | `dest` token **PASS** |
| extract vars | `getVariables` on binary | `[op1, op2]` | `[op1, op2]` **PASS** |
| extract vars | binary with literals | `[]` (no variables to extract) | `[]` **PASS** |
| extract vars | binary with mixed tokens | `[op1]` | `[op1]` **PASS** |
| extract vars | unary with variable | `[op]` | `[op]` **PASS** |
| extract vars | unary with literal | `[]` | `[]` **PASS** |
| extract vars | assignment with variable | `[op]` | `[op]` **PASS** |
| extract vars | assignment with literal | `[]` | `[]` **PASS** |
| empty list | `getInstructions emptyInstructions` | `[]` | `[]` **PASS** |
| empty live | `getLiveVariables emptyInstructions` | `[]` | `[]` **PASS** |
| wrappers | `fromArraysInstructions` insts only | stores the instructions | stored **PASS** |
| wrappers | `fromArraysInstructions` live only | stores `["a", "b"]` | stored **PASS** |
| wrappers | `fromArraysInstructions` both | stores both lists properly | stored **PASS** |
| get lists | `getInstructions` on populated | returns the list of insts | matches **PASS** |
| get lists | `getLiveVariables` on populated | returns the list of live vars | matches **PASS** |
| show wrapper | `showInstructions []` | `"Instructions: \n"` | `"Instructions: \n"` **PASS** |
| show wrapper | `showInstructions [assignIns]` | prints with prefix | matches expected **PASS** |
| show wrapper | multiple instructions | lines split by newline | matches expected **PASS** |
| show live | `showLiveVars []` | `"Live: "` | `"Live: "` **PASS** |
| show live | `showLiveVars ["x"]` | `"Live: x"` | `"Live: x"` **PASS** |
| show live | `showLiveVars ["x", "y"]` | `"Live: x, y"` | `"Live: x, y"` **PASS** |
| full print | `show (fromArraysInstructions ...)` | combines instructions and live line | combined correctly **PASS** |