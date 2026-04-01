# InstructionBuffer-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — empty buffer | `InstructionBuffer()` | `instructions` is empty `dllist`, `live_objects` is empty `dllist`, `occurred_variables` is empty `set` | |
| `add_instruction()` — single instruction | `buf.add_instruction(instr)` | `buf.list_instructions()` returns `[instr]` | |
| `add_instruction()` — multiple instructions | Add 3 instructions in order | `buf.list_instructions()` returns all 3 in insertion order | |
| `add_live_object()` — single object | `buf.add_live_object("a")` | `buf.list_live_objects()` returns `["a"]` | |
| `add_live_object()` — multiple objects | Add `"a"`, `"b"`, `"c"` in order | `buf.list_live_objects()` returns `["a", "b", "c"]` | |
| `list_instructions()` — empty buffer | `InstructionBuffer().list_instructions()` | `[]` | |
| `list_instructions()` — populated buffer | Buffer with 2 instructions added | List of those 2 instruction objects in insertion order | |
| `list_live_objects()` — empty buffer | `InstructionBuffer().list_live_objects()` | `[]` | |
| `list_live_objects()` — populated buffer | Buffer with `"a"` and `"b"` added | `["a", "b"]` | |
| `get_instructions()` — returns dllist | `buf.get_instructions()` after adding an instruction | Returns a `dllist` containing the instruction | |
| `get_live_objects()` — returns dllist | `buf.get_live_objects()` after adding a live object | Returns a `dllist` containing the live object | |
| `set_occurred_variables()` — sets correctly | `buf.set_occurred_variables({"a", "b"})` | `buf.get_occurred_variables() == {"a", "b"}` | |
| `get_occurred_variables()` — empty on construction | `InstructionBuffer().get_occurred_variables()` | `set()` | |
| `get_occurred_variables()` — after set | `buf.set_occurred_variables({"x"})`, then `buf.get_occurred_variables()` | `{"x"}` | |