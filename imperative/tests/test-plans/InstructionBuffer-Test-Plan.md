# InstructionBuffer-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — empty buffer | `InstructionBuffer()` | `instructions` is empty `dllist`, `live_objects` is empty `dllist`, `occurred_variables` is empty `set` | `instructions` is empty `dllist`, `live_objects` is empty `dllist`, `occurred_variables` is empty `set` **PASS** |
| `add_instruction()` — single instruction | `buf.add_instruction(instr)` | `buf.list_instructions()` returns `[instr]` | `buf.list_instructions()` returns `[instr]` **PASS** |
| `add_instruction()` — multiple instructions | Add 3 instructions in order | `buf.list_instructions()` returns all 3 in insertion order | `buf.list_instructions()` returns all 3 in insertion order **PASS** |
| `add_live_object()` — single object | `buf.add_live_object("a")` | `buf.list_live_objects()` returns `["a"]` | `buf.list_live_objects()` returns `["a"]` **PASS**|
| `add_live_object()` — multiple objects | Add `"a"`, `"b"`, `"c"` in order | `buf.list_live_objects()` returns `["a", "b", "c"]` | `buf.list_live_objects()` returns `["a", "b", "c"]` **PASS** |
| `list_instructions()` — empty buffer | `InstructionBuffer().list_instructions()` | `[]` | `[]` **PASS** |
| `list_instructions()` — populated buffer | Buffer with 2 instructions added | List of those 2 instruction objects in insertion order | List of those 2 instruction objects in insertion order **PASS** |
| `list_live_objects()` — empty buffer | `InstructionBuffer().list_live_objects()` | `[]` | `[]` **PASS** |
| `list_live_objects()` — populated buffer | Buffer with `"a"` and `"b"` added | `["a", "b"]` | `["a", "b"]` **PASS** |
| `get_instructions()` — returns dllist | `buf.get_instructions()` after adding an instruction | Returns a `dllist` containing the instruction | Returns a `dllist` containing the instruction **PASS** |
| `get_live_objects()` — returns dllist | `buf.get_live_objects()` after adding a live object | Returns a `dllist` containing the live object | Returns a `dllist` containing the live object **PASS** |
| `set_occurred_variables()` — sets correctly | `buf.set_occurred_variables({"a", "b"})` | `buf.get_occurred_variables() == {"a", "b"}` | `buf.get_occurred_variables() == {"a", "b"}` **PASS** |
| `get_occurred_variables()` — empty on construction | `InstructionBuffer().get_occurred_variables()` | `set()` | `set()` **PASS** |
| `get_occurred_variables()` — after set | `buf.set_occurred_variables({"x"})`, then `buf.get_occurred_variables()` | `{"x"}` | `{"x"}` **PASS** |