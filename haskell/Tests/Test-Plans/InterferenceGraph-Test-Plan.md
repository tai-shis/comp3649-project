# InterferenceGraph-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| `createVariable` — correct name | `getName (createVariable "x")` | `"x"` | `"x"` **PASS** |
| `createVariable` — empty neighbors | `getNeighbors (createVariable "x")` | `empty` | `empty` **PASS** |
| `createGraph` — empty vertices | `getVertices createGraph` | `[]` | `[]` **PASS** |
| `Show Variable` — no neighbors | `show (createVariable "x")` | `"x -> "` | `"x -> "` **PASS** |
| `Show Variable` — with neighbors | `show` on variable after edges added | `"a -> "b""` |`"a -> "b""` **PASS** |
| `Show Graph` — empty graph | `show createGraph` | `"Interference Graph: \n"` | `"Interference Graph: \n"` **PASS** |
| `Show Graph` — populated graph | `show` on graph with two variables | `"Interference Graph: \na -> "b"\nb -> "a""` | `"Interference Graph: \na -> "b"\nb -> "a""` **PASS** |
| `Eq Variable` — equal variables | `createVariable "x" == createVariable "x"` | `True` | `True` **PASS** |
| `Eq Variable` — different names | `createVariable "x" /= createVariable "y"` | `True` | `True` **PASS** |
| `Eq Graph` — equal graphs | `createGraph == createGraph` | `True` | `True` **PASS** |
| `Eq Graph` — different graphs | `buildGraph ["x"] [] /= buildGraph ["y"] []` | `True` | `True` **PASS** |
| `addEdge` — both nodes exist, a has b as neighbor | `hasNeighbor (addEdge graph "a" "b") "a" "b"` | `True` | `True` **PASS** |
| `addEdge` — both nodes exist, b has a as neighbor | `hasNeighbor (addEdge graph "a" "b") "b" "a"` | `True` | `True` **PASS** |
| `addEdge` — first node missing | `addEdge (Graph [createVariable "b"]) "a" "b"` | `Graph [createVariable "b"]` | `Graph [createVariable "b"]` **PASS** |
| `addEdge` — second node missing | `addEdge (Graph [createVariable "a"]) "a" "b"` | `Graph [createVariable "a"]` | `Graph [createVariable "a"]` **PASS** |
| `addEdge` — neither node exists | `addEdge createGraph "a" "b"` | `createGraph` | `createGraph` **PASS** |
| `addEdge` — self edge | `addEdge (Graph [createVariable "x"]) "x" "x"` | `Graph [createVariable "x"]` | `Graph [createVariable "x"]` **PASS** |
| `addEdge` — duplicate edge | `addEdge (addEdge graph "a" "b") "a" "b" == addEdge graph "a" "b"` | `True` | `True` **PASS** |
| `addEdge` — three nodes, two edges | `hasNeighbor` checks on `"a"`, `"b"`, `"c"` after two `addEdge` calls | `"a"` neighbors `"b"` and `"c"`, `"b"` and `"c"` not neighbors of each other | `"a"` neighbors `"b"` and `"c"`, `"b"` and `"c"` not neighbors of each other **PASS** |
| `buildGraph` — empty variables and liveness | `buildGraph [] []` | `createGraph` | `createGraph` **PASS** |
| `buildGraph` — nodes created for all variables | `hasVertex` checks on `buildGraph ["a", "b", "x"] []` | `True` for `"a"`, `"b"`, and `"x"` | `True` for `"a"`, `"b"`, and `"x"` **PASS** |
| `buildGraph` — edge between two live vars | `hasNeighbor (buildGraph ["a","b"] [[Live "a", Live "b"]]) "a" "b"` | `True` | `True` **PASS** |
| `buildGraph` — no edge for unlive variable | `hasNeighbor (buildGraph ["a","b"] [[Live "a", Unlive "b"]]) "a" "b"` | `False` | `False` **PASS** |
| `buildGraph` — no edge for isolated variable | `getNeighbors` on `"x"` in `buildGraph ["a","b","x"] [[Live "a", Live "b"]]` | `empty` | `empty` **PASS** |
| `buildGraph` — no duplicate edges | `toList (getNeighbors` on `"a"` after same pair live on two lines`)` | `["b"]` | `["b"]` **PASS** |
| `buildGraph` — no self edges | `getNeighbors` on `"a"` in `buildGraph ["a"] [[Live "a"]]` | `empty` | `empty` **PASS** |