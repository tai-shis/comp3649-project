### Key Data Structs
1. Class/Structure representing a single three-address instruction (address representation : list of objects + list of objects that are live at end of file)
```
class intermediate_code {
    list_of_objects:
    list_of_live_objects:
}

Code Rep: I -> 3AS LL
3AddrInstrSequence: 3AS -> 3A [3AS]
3AddrInstr: 
3A -> D = S OP S
3A -> D = OP S
3A -> D = S
``` 
**NOTE**: Return exceptions from functions when an unexpected symbol is seen
2. Class/Structure representing a single assembly language instruction (address representation : list of asm language objects)
3. 

**Note:** Add support routines (constructors, destructors, getters, setters, parsers) for querying data structures 1 and 2.
 - Routine(s) to print (1) and (2) in human-readable format will be helpful.
