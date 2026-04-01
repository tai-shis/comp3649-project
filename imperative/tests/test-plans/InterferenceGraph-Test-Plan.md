# InterferenceGraph-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — empty graph | `InterferenceGraph()` | `interference_graph` has no nodes or edges, `colors` is `{}` | |
| `build_graph()` — nodes added for all variables | `variables = {"a", "b", "x"}` | Graph contains nodes `"a"`, `"b"`, `"x"` | |
| `build_graph()` — all colors initialized to None | `variables = {"a", "b"}` | `colors == {"a": None, "b": None}` | |
| `build_graph()` — edge added between two live vars | Liveness line: `{"a": 1, "b": 1}` | Edge exists between `"a"` and `"b"` | |
| `build_graph()` — no edge for unlive variable | Liveness line: `{"a": 1, "b": 2}` | No edge between `"a"` and `"b"` (`b` is unlive, state == 2) | |
| `build_graph()` — no edge for defined variable | Liveness line: `{"a": 0, "b": 1}` | No edge between `"a"` and `"b"` (`a` is defined, state == 2) | |
| `build_graph()` — no self-edges | Any liveness with a single live variable | No self-edges in graph | |
| `build_graph()` — no duplicate edges | Same pair of live vars appearing on multiple lines | Only one edge between the pair | |
| `_is_solved()` — returns False when colors are None | Graph with uncolored nodes | Returns `False` | |
| `_is_solved()` — returns False when neighbors share color | Two connected nodes with same color | Returns `False` | |
| `_is_solved()` — returns True when properly colored | All nodes colored, no neighbors share color | Returns `True` | |
| `_is_solved()` — returns True on empty graph | `InterferenceGraph()` with no nodes | Returns `True` | |
| `_possible_colors()` — all colors available | Node with no colored neighbors, `n = 3` | Returns `{0, 1, 2}` | |
| `_possible_colors()` — excludes neighbor colors | Node whose neighbor is colored `0`, `n = 3` | Returns `{1, 2}` | |
| `_possible_colors()` — no colors available | Node whose neighbors use all `n` colors | Returns `set()` | |
| `_possible_colors()` — ignores uncolored neighbors | Node with one uncolored neighbor and one colored `0`, `n = 2` | Returns `{1}` (uncolored neighbor not excluded) | |
| `color_graph()` — 2-colorable graph | Two connected nodes, `n = 2` | Both nodes colored with different colors, no exception raised | |
| `color_graph()` — 3-colorable triangle | Three mutually connected nodes, `n = 3` | All three nodes colored with distinct colors | |
| `color_graph()` — insufficient colors raises error | Triangle graph (3 nodes, all connected), `n = 2` | Raises `ValueError` | |
| `color_graph()` — isolated node colored | Single node, no edges, `n = 1` | Node assigned color `0` | |
| `print_variable_interference_table()` — correct format | Graph with nodes `"a"` and `"b"` connected | Prints `"a: b"` and `"b: a"` in sorted order | |
| `print_variable_interference_table()` — isolated node | Node `"x"` with no edges | Prints `"x: "` with empty neighbor list | |
| `print_variable_interference_table()` — sorted output | Nodes `"c"`, `"a"`, `"b"` | Printed in alphabetical order | |
| `print_register_colouring_table()` — correct format | Node `"a"` colored `0`, `n = 1` | Prints `"R0: a"` | |
| `print_register_colouring_table()` — multiple vars per register | Nodes `"a"` and `"b"` both colored `0`, `n = 1` | Prints `"R0: a, b"` | |
| `print_register_colouring_table()` — empty register | `n = 2`, only one register used | Unused register prints `"R1: "` with empty list | |
| `__str__()` — contains nodes | Graph with nodes `"a"`, `"b"` | Output string contains `"Nodes:"` and both node names | |
| `__str__()` — contains edges | Graph with edge between `"a"` and `"b"` | Output string contains `"Edges:"` and the edge | |
| `__str__()` — contains colors | Graph with `colors = {"a": 0}` | Output string contains `"Colors:"` and `{"a": 0}` | |