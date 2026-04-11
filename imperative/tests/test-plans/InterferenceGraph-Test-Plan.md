# InterferenceGraph-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| Construction — empty graph | `InterferenceGraph()` | `interference_graph` has no nodes or edges, `colors` is `{}` | Passed — `len(nodes) == 0`, `len(edges) == 0`, `colors == {}` |
| `build_graph()` — nodes added for all variables | `variables = {"a", "b", "x"}` | Graph contains nodes `"a"`, `"b"`, `"x"` | Passed — `"a"`, `"b"`, `"x"` all present in graph nodes |
| `build_graph()` — all colors initialized to None | `variables = {"a", "b"}` | `colors == {"a": None, "b": None}` | Passed — `colors["x"] is None` and `colors["a"] is None` |
| `build_graph()` — edge added between two live vars | Liveness line: `{"a": 1, "b": 1}` | Edge exists between `"a"` and `"b"` | Passed — `has_edge("a", "b")` is `True` |
| `build_graph()` — no edge for unlive variable | Liveness line: `{"a": 1, "b": 2}` | No edge between `"a"` and `"b"` (`b` is unlive, state == 2) | Passed — `has_edge("a", "b")` is `False` |
| `build_graph()` — no edge for defined variable | Liveness line: `{"a": 0, "b": 1}` | No edge between `"a"` and `"b"` (`a` is defined, state == 2) | Passed — `has_edge("x", "a")` is `False` |
| `build_graph()` — no self-edges | Any liveness with a single live variable | No self-edges in graph | Passed — `has_edge(node, node)` is `False` for all nodes |
| `build_graph()` — no duplicate edges | Same pair of live vars appearing on multiple lines | Only one edge between the pair | Passed — `number_of_edges("a", "b") == 1` |
| `_possible_colors()` — all colors available | Node with no colored neighbors, `n = 3` | Returns `{0, 1, 2}` | Passed — returns `{0, 1, 2}` |
| `_possible_colors()` — excludes neighbor colors | Node with two colored neighbors (`a=0`, `b=1`), `n = 3` | Returns `{2}` | Passed — returns `{2}` |
| `_possible_colors()` — no colors available | Node whose neighbors use all `n` colors | Returns `set()` | Passed — returns `set()` |
| `_possible_colors()` — ignores uncolored neighbors | Node with one uncolored neighbor and one colored `0`, `n = 2` | Returns `{1}` (uncolored neighbor not excluded) | Passed — returns `{1}` |
| `color_graph()` — 2-colorable graph | Two connected nodes, `n = 2` | Both nodes colored with different colors, no exception raised | Passed — all connected pairs have different colors, no exception raised |
| `color_graph()` — 3-colorable triangle | Three mutually connected nodes, `n = 3` | All three nodes colored with distinct colors | Passed — `colors["a"]`, `colors["b"]`, `colors["c"]` are all distinct |
| `color_graph()` — insufficient colors raises error | Triangle graph (3 nodes, all connected), `n = 2` | Raises `ValueError` | Passed — `ValueError` raised |
| `color_graph()` — isolated node colored | Single node, no edges, `n = 1` | Node assigned color `0` | Passed — `colors["x"] == 0` |
| `print_variable_interference_table()` — correct format | Graph with nodes `"a"` and `"b"` connected | Prints `"a: b"` and `"b: a"` in sorted order | Passed — output contains `"a: b"` and `"b: a"` |
| `print_variable_interference_table()` — isolated node | Node `"x"` with no edges | Prints `"x: "` with empty neighbor list | Passed — output contains `"x: "` |
| `print_variable_interference_table()` — sorted output | Nodes `"c"`, `"a"`, `"b"` | Printed in alphabetical order | Passed — node names appear in alphabetical order |
| `print_register_colouring_table()` — correct format | Node `"a"` colored `0`, `n = 1` | Prints `"R0: a"` | Passed — output contains `"R0: a"` |
| `print_register_colouring_table()` — multiple vars per register | Nodes `"a"` and `"b"` both colored `0`, `n = 1` | Prints `"R0: a, b"` | Passed — output contains `"R0: a, b"` |
| `print_register_colouring_table()` — empty register | `n = 2`, only one register used | Unused register prints `"R1: "` with empty list | Passed — output contains `"R1: "` |
| `__str__()` — contains nodes | Graph with nodes `"a"`, `"b"` | Output string contains `"Nodes:"` and both node names | Passed — output contains `"Nodes:"` |
| `__str__()` — contains edges | Graph with edge between `"a"` and `"b"` | Output string contains `"Edges:"` and the edge | Passed — output contains `"Edges:"` |
| `__str__()` — contains colors | Graph with `colors = {"a": 0}` | Output string contains `"Colors:"` and `{"a": 0}` | Passed — output contains `"Colors:"` |