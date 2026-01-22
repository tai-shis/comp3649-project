graph coloring:
from start node: 
    mark start node with 0
    mark all connected nodes with self +1

check new nodes nodes 
    check all connected nodes for itself's value
    if a connected node has the same value as itself,
        set value +1
    then, continue with marking (mark empty connected with +1)