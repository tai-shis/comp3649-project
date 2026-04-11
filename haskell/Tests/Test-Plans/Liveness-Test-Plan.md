# Liveness Test Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| print states | `show (Defined "x")` | `"x: defined"` | `"x: defined"` **PASS** |
| print states | `show (Live "x")` | `"x: live"` | `"x: live"` **PASS** |
| print states | `show (Unlive "x")` | `"x: unlive"` | `"x: unlive"` **PASS** |
| equality | `Defined "x" == Defined "x"` | `True` | `True` **PASS** |
| equality | `Live "x" == Live "x"` | `True` | `True` **PASS** |
| equality | `Unlive "x" == Unlive "x"` | `True` | `True` **PASS** |
| inequality | `Defined "x" == Live "x"` | `False` | `False` **PASS** |
| inequality | `Defined "x" == Unlive "x"` | `False` | `False` **PASS** |
| inequality | `Live "x" == Unlive "x"` | `False` | `False` **PASS** |
| inequality | different variable names | `False` | `False` **PASS** |
| getters | `getLivenessName` on Defined | `"x"` | `"x"` **PASS** |
| getters | `getLivenessName` on Live | `"x"` | `"x"` **PASS** |
| getters | `getLivenessName` on Unlive | `"x"` | `"x"` **PASS** |
| extraction | `namesFromLiveness []` | `[]` | `[]` **PASS** |
| extraction | mixed list of states | extracts all variable names | `["x", "a", "b"]` **PASS** |
| boolean flags | `isLive` on live state | `True` (False for others) | works correctly **PASS** |
| boolean flags | `isDefined` on defined state | `True` (False for others) | works correctly **PASS** |
| boolean flags | `isUnlive` on unlive state | `True` (False for others) | works correctly **PASS** |
| print blocks | `showLivenessStates []` | `""` | `""` **PASS** |
| print blocks | single line array | `"x: defined, a: live\n"` | matches expected **PASS** |
| print blocks | multi line array | prints with newlines | matches expected **PASS** |
| logic | empty instructions | `[[]]` (one empty state block) | matches **PASS** |
| logic | single assign (operand live) | x defined, a live | states are correct **PASS** |
| logic | single assign (no live vars) | x defined, a unlive | states are correct **PASS** |
| logic | binary instruction | x defined, a and b live | states are correct **PASS**|
| logic | var defined then used | x defined on 0, live on 1 | states are correct **PASS** |
| logic | var unlive after last use | a unlive immediately | marked unlive **PASS** |
| logic | array length check | 3 instructions -> length 4 | length is 4 **PASS** |