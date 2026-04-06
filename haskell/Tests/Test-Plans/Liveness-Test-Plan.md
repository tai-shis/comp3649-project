# Liveness-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `Show LivenessState` — Defined | `show (Defined "x")` | `"x: defined"` | `"x: defined"` **PASS** |
| `Show LivenessState` — Live | `show (Live "x")` | `"x: live"` | `"x: live"` **PASS** |
| `Show LivenessState` — Unlive | `show (Unlive "x")` | `"x: unlive"` | `"x: unlive"` **PASS** |
| `Eq LivenessState` — Defined == Defined, same name | `Defined "x" == Defined "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — Live == Live, same name | `Live "x" == Live "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — Unlive == Unlive, same name | `Unlive "x" == Unlive "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — Defined == Live, same name | `Defined "x" == Live "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — Live == Defined, same name | `Live "x" == Defined "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — Defined == Unlive, same name | `Defined "x" == Unlive "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — Live == Unlive, same name | `Live "x" == Unlive "x"` | `True` | `True` **PASS** |
| `Eq LivenessState` — different names | `Defined "x" == Defined "y"` | `False` | `False` **PASS** |
| `getLivenessName` — Defined | `getLivenessName (Defined "x")` | `"x"` | `"x"` **PASS** |
| `getLivenessName` — Live | `getLivenessName (Live "x")` | `"x"` | `"x"` **PASS** |
| `getLivenessName` — Unlive | `getLivenessName (Unlive "x")` | `"x"` | `"x"` **PASS** |
| `namesFromLiveness` — empty list | `namesFromLiveness []` | `[]` | `[]` **PASS** |
| `namesFromLiveness` — mixed states | `namesFromLiveness [Defined "x", Live "a", Unlive "b"]` | `["x", "a", "b"]` | `["x", "a", "b"]`**PASS** |
| `isLive` — Live state | `isLive (Live "x")` | `True` | `True` **PASS** |
| `isLive` — Defined state | `isLive (Defined "x")` | `False` | `False` **PASS** |
| `isLive` — Unlive state | `isLive (Unlive "x")` | `False` | `False` **PASS** |
| `isDefined` — Defined state | `isDefined (Defined "x")` | `True` | `True` **PASS** |
| `isDefined` — Live state | `isDefined (Live "x")` | `False` | `False` **PASS** |
| `isDefined` — Unlive state | `isDefined (Unlive "x")` | `False` | `False` **PASS** |
| `isUnlive` — Unlive state | `isUnlive (Unlive "x")` | `True` | `True` **PASS** |
| `isUnlive` — Live state | `isUnlive (Live "x")` | `False` | `False` **PASS** |
| `isUnlive` — Defined state | `isUnlive (Defined "x")` | `False` | `False` **PASS** |
| `showLivenessStates` — empty list | `showLivenessStates []` | `""` | `""` **PASS** |
| `showLivenessStates` — single line | `showLivenessStates [[Defined "x", Live "a"]]` | `"x: defined, a: live\n"` | `"x: defined, a: live\n"` **PASS** |
| `showLivenessStates` — multiple lines | `showLivenessStates [[Defined "x"], [Live "a"]]` | `"x: defined\na: live\n"` | "x: defined\na: live\n"` **PASS** |
| `determineLiveness` — empty instructions | `determineLiveness emptyInstructions` | `[[]]` (one empty liveness state for the live section) | `[[]]` (one empty liveness state for the live section) **PASS** |
| `determineLiveness` — single assignment, operand live | `determineLiveness` on `"x = a"` with `live: a` | Instruction line: `[Defined "x", Live "a"]`, live section: `[Live "a"]` | Instruction line: `[Defined "x", Live "a"]`, live section: `[Live "a"]` **PASS** |
| `determineLiveness` — single assignment, no live vars | `determineLiveness` on `"x = a"` with no live vars | Instruction line: `x` defined, `a` unlive | Instruction line: `x` defined, `a` unlive **PASS** |
| `determineLiveness` — single binary instruction | `determineLiveness` on `"x = a + b"` with `live: a, b` | Instruction line: `x` defined, `a` and `b` live | Instruction line: `x` defined, `a` and `b` live **PASS**|
| `determineLiveness` — variable defined then used | `determineLiveness` on `"x = a\ny = x"` with `live: x` | `x` defined on line 0, live on line 1 | `x` defined on line 0, live on line 1 **PASS** |
| `determineLiveness` — variable unlive after last use | `determineLiveness` on `"x = a\ny = b"` with `live: b` | `a` is unlive on line 0 as it is not used again | `a` is unlive on line 0 as it is not used again **PASS** |
| `determineLiveness` — result length | `determineLiveness` on 3 instructions | Returns list of length 4 (3 instructions + live section) | Returns list of length 4 (3 instructions + live section) **PASS** |