# Interference Graph Test Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| node creation | `getName (createVariable "x")` | `"x"` | `"x"` **PASS** |
| node creation | `getNeighbors` on new var | `empty` set | `empty` **PASS** |
| graph creation| `getVertices createGraph` | `[]` | `[]` **PASS** |
| printing vars | `show` on var with no edges | `"x -> "` | `"x -> "` **PASS** |
| printing vars | `show` on connected var | `"a -> "b""` | `"a -> "b""` **PASS** |
| printing graph| empty graph | `"Interference Graph: \n"` | `"Interference Graph: \n"` **PASS** |
| printing graph| populated graph | prints all edges correctly | matches expected **PASS** |
| equality | `createVariable "x" == "x"` | `True` | `True` **PASS** |
| inequality | `createVariable "x" /= "y"` | `True` | `True` **PASS** |
| graph eq | empty == empty | `True` | `True` **PASS** |
| graph ineq | graph x /= graph y | `True` | `True` **PASS** |
| manual edges | check neighbors after addEdge | a has b, b has a | confirmed **PASS** |
| edge failures | addEdge if first node missing | fails safely (graph unchanged) | unchanged **PASS** |
| edge failures | addEdge if second node missing| fails safely | unchanged **PASS** |
| edge failures | addEdge on empty graph | returns empty graph | empty graph **PASS** |
| bad edges | addEdge self loop ("x" to "x") | ignores it | ignored **PASS** |
| bad edges | duplicate edge | ignores it | ignored **PASS** |
| multiple edges| adding 2 edges to a | a connects to b and c | connects **PASS** |
| builder edge | `buildGraph [] []` | returns empty graph | empty graph **PASS** |
| builder nodes | buildGraph with 3 vars | creates all 3 vertices | created **PASS** |
| builder logic | variables live at same time | draws edge between a and b | edge exists **PASS** |
| builder logic | isolated variable | stays disconnected | no edges **PASS** |
| builder logic | same vars live on multiple lines | doesn't duplicate the edge | no duplicates **PASS** |
| builder logic | prevents self loops | no edges from "a" to "a" | no self loops **PASS** |
