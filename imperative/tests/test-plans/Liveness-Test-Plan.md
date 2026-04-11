# Liveness-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — empty buffer | `Liveness(InstructionBuffer())` | `get_liveness()` returns `[{}]` (one empty dict for the live section) | `get_liveness()` returns `[{}]` (one empty dict for the live section) **PASS** |
| Construction — liveness determined on init | `Liveness(buffer)` with one instruction | `liveness` is populated without calling any method manually | `liveness` is populated without calling any method manually **PASS** |
| `_determine_initial_liveness()` — no live objects | Buffer with no live objects | Returns `[]`, liveness contains one empty dict | Returns `[]`, liveness contains one empty dict **PASS** |
| `_determine_initial_liveness()` — single live object | Buffer with `live: a` | Returns `["a"]`, liveness contains `{"a": 1}` | Returns `["a"]`, liveness contains `{"a": 1}` **PASS** |
| `_determine_initial_liveness()` — multiple live objects | Buffer with `live: a, b` | Returns `["a", "b"]`, liveness contains `{"a": 1, "b": 1}` | Returns `["a", "b"]`, liveness contains `{"a": 1, "b": 1}` **PASS** |
| `_mark_liveness()` — assignment, no carry vars | `variables = [dest, op1]`, `carry_vars = []` | `dest` marked `defined (0)`, `op1` marked `unlive (2)` | `dest` marked `defined (0)`, `op1` marked `unlive (2)` **PASS** |
| `_mark_liveness()` — assignment, op1 in carry vars | `variables = [dest, op1]`, `carry_vars = [op1.value]` | `dest` marked `defined (0)`, `op1` marked `live (1)` | `dest` marked `defined (0)`, `op1` marked `live (1)` **PASS** |
| `_mark_liveness()` — binary, no carry vars | `variables = [dest, op1, op2]`, `carry_vars = []` | `dest` marked `defined (0)`, `op1` and `op2` marked `unlive (2)` | `dest` marked `defined (0)`, `op1` and `op2` marked `unlive (2)` **PASS** |
| `_mark_liveness()` — binary, both operands in carry vars | `variables = [dest, op1, op2]`, `carry_vars = [op1.value, op2.value]` | `dest` marked `defined (0)`, `op1` and `op2` marked `live (1)` | `dest` marked `defined (0)`, `op1` and `op2` marked `live (1)` **PASS** |
| `_mark_liveness()` — carry vars cleared and repopulated | `variables = [dest, op1]`, `carry_vars = ["x"]` before call | After call, `carry_vars` contains only non-defined, non-unlive vars from current line | After call, `carry_vars` contains only non-defined, non-unlive vars from current line **PASS** |
| `_determine_liveness()` — single assignment | Buffer: `"x = a\n"`, `live: a` | Liveness: `[{"a": 1}, {"x": 0, "a": 1}, {"a": 1}]` | Liveness: `[{"a": 1}, {"x": 0, "a": 1}, {"a": 1}]` **PASS** |
| `_determine_liveness()` — single binary instruction | Buffer: `"x = a + b\n"`, `live: a, b` | `x` defined, `a` and `b` live on instruction line | `x` defined, `a` and `b` live on instruction line **PASS** |
| `_determine_liveness()` — variable defined then used | Buffer: `"x = a\ny = x\n"`, `live: x` | `x` is defined on first line, live on second | `x` is defined on first line, live on second **PASS** |
| `_determine_liveness()` — variable unlive after last use | Buffer: `"x = a\ny = b\n"`, `live: b` | `a` is unlive on second line as it is not used again | `a` is unlive on second line as it is not used again **PASS** |
| `_determine_liveness()` — instructions processed in reverse | Buffer with 3 instructions | Liveness list length equals number of instructions + 1 (for live section) | Liveness list length equals number of instructions + 1 (for live section) **PASS** |
| `get_liveness()` — returns list of dicts | `Liveness(buffer).get_liveness()` | Returns a `list` of `dict[str, int]` | Returns a `list` of `dict[str, int]` **PASS** |
| `get_liveness()` — correct length | Buffer with 3 instructions | Returns list of length 4 (3 instructions + live section) | Returns list of length 4 (3 instructions + live section) **PASS** |
| `liveness_info()` — defined state string | Instruction where `x` is destination | String for that line contains `"x: defined"` | String for that line contains `"x: defined"` **PASS** |
| `liveness_info()` — live state string | Variable carried as live | String for that line contains `"var: live"` | String for that line contains `"var: live"` **PASS** |
| `liveness_info()` — unlive state string | Variable not in carry vars | String for that line contains `"var: unlive"` | String for that line contains `"var: unlive"` **PASS** |
| `liveness_info()` — correct format | Any buffer | Each entry formatted as `"[var: state, ...]"` | Each entry formatted as `"[var: state, ...]"` **PASS** |
| `__str__()` — correct number of lines | Buffer with 2 instructions | Output has 3 lines (2 instructions + end of code block) | Output has 3 lines (2 instructions + end of code block) **PASS** |
| `__str__()` — end of code block line | Any buffer | Last line contains `"End of code block:"` | Last line contains `"End of code block:"` **PASS** |
| `__str__()` — instruction index prefix | Buffer with instructions | Each instruction line prefixed with its index starting at `0` | Each instruction line prefixed with its index starting at `0` **PASS** |