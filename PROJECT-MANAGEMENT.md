# Project Management

## Planning
### Week 3
<small>Last Updated: 22/01/2026</small>

#### Develop Initial Data Structures and Support Routines
- Objects required
  - Token
    - Holds type and if applicable name/value
  - Scanner 
    - Creates a list of Token objects by reading one(1) line from input file at a time
  - Parser
    - Reads Tokens from scanner as needed (i.e. one token at a time)
    - Checks Token validity
  - Three Address Instruction (Int Code)
    - Holds source, destination, operand
#### Read and Validate the Input File
- Scanner
  - Takes input file and tokenizes the input into a list of token objects
  - Result will be a list of tokens representing operators, operands, and literals
  - Remove all white space, include some delimiter [to be decided] to indicate end of instruction/line
- Parser
  - Requests one (1) token at a time from Scanner and validates it
  - Creates list of 3 Address Instructions from valid Tokens
  - **Note:** if any Tokens are not valid and exception will be thrown and the code generation will terminate

### Week 4
<small>Last Updated: 12/02/2026</small>

- Check all **Week 3** code to ensure it is fully tested anf functioning as expected
- Implement liveness algorithm
  - Scans the three-address-instructions to determine when it is defined and when it is last used
- Create interference graph
  - Based on liveness, interference graph will show which variables are live at the same point in the code execution and assign an 'edge' to connect the variables that are live at the same time.

### Week 5
<small>Last Updated: 12/02/2026</small>

- Begin initial design process of graph colouring algorithm
  - For every live variable, a 'colour' (i.e. integer from 0 to n) will be assigned to a variable that is live
  - For every variable that interferes with any other live variable, they will have a different number *n*
  - Two variables can be live tat the same time as long as they are not interfering with each other (i.e. do not have a direct connection through an edge on the graph)

### Week 6
<small>Last Updated: 12/02/2026</small>

- Complete graph colouring algorithm
- Begin process of generating assembly language output
  - Iterate through the list of three-address-instructions and generate the corressponding assembly code
  - Generally, this is going to be unoptimized, but the *goal* is to have some optimizations built in at some point before the Haskell implementation begins
  
### Week 7
<small>Last Updated: 12/02/2026</small>

- Finish graph colouring algorithm
- Ensure testing is complete and thorough. Update any tests to ensure the most coverage as possible and promptly fix any issues that arise

### Week 8
<small>Last Updated: 01/03/2026</small>

- Begin Haskell implementation

## High-level Design Architecture
<small>Last Updated: 01/03/2026</small>

### Main Data Structures
- Token
  - Token contains a value (str) and a type (Int). The ```type``` field is mapped to a dictionary with options such as **variable, literal, operator, equals, etc...**.
- Instruction
  - A representation of a single three-address-instruction. There are three (3) types not including the ```invalid``` type/classification for error handling. The types are: **binary_operator: 0, unary_operator: 1, assignment: 2**. 
- Instruction Buffer
  - An object that manages the list of valid instructions using a doubly linked list from the Python package [dllist](https://pypi.org/project/dllist/). It also tracks the *occurred variables* and *live objects* that will be used when creating the interference graph and later colouring that graph.
- ASMInstruction
  - A simple object used by the main assembly code generator to represent a single assembly instruction. It stores strings representing the following: *op_code* (i.e. MOV, ADD, MUL), *op1* (i.e. a, #1, b), and *op2* (i.e. R0).

### Modules
#### Input Module(s)
- Scanner
  - Reads the raw input stream and tokenizes symbols it deems valid. Builds up a buffer of valid Tokens.
- Parser
  - Reads Tokens from the Scanner, checks that the sequence of the Tokens is valid against rules such as valid assignments or binary operations and builds the InstructionBuffer with Instructions.
#### Intermediate Module(s)
- Liveness
  - Determines which variables are still live at the end of the given input file. The program will use this data to ensure the registers these variables are stored in are not cleared as they are likely being used in another file at another point in the program's execution.
- InterferenceGraph
  - Uses result of the Liveness to build a graph where each node represents a variable, and edges connecting nodes represent the variables that are live at the same time (i.e. are interfering). This object has the ability to colour the graph, that determines which registers to use for each variable. 
#### Generator Module(s)
- ASMGenerator
  - Converts the intermediate code into assembly instructions by mapping variables to their assigned registers based on the InterferenceGraph's colouring. The result will be an output ```.s``` file containing instructions for the entirety of the input file.

### Phases
1. Parsing: The Parser uses the Scanner's Tokens to fill the InstructionBuffer with valid Instructions.
2. Intermediate Code: The Liveness module processes Instructions within the InstructionBuffer to allocate registers to variables.
3. Generation: ASMGenerator takes the InstructionBuffer and InterferenceGraph data to produce assembly representations of each Instruction. These instructions are placed into a list of all assembly instructions and outputs them to the ```assmebly.s``` file.


## High-level Testing Framework
<small>Last Updated: 01/03/2026</small>

~~With the current state of the project, our testing framework is to develop test cases as we go.~~

The group decided on a system where we will implement tests as new features are developed. To minimize conflicts with other coursework, there are no hard rules on which member develops tests. The general idea for our framework is for a member to partially or fully implement a feature, and once that feature has been completed, tests are developed for it. The tests can be developed by any member of the group, including the person who developed the feature.
### Guidelines
- **Always** develop tests on a separate branch from the *feature* branch. Test branches must be formatted the following way: *test/feature-name-**tests*** \
For example: \
Feature branch: *feat/scanner* \
- Merge test branches into the feature branch, and then the feature branch can be dealt with afterwards. We are treating the test branches as sub-branches to the feature branch, not an extension of main.
- It is ideal for another member of the group to review and accept the PR that was opened on the test branch. However, if timeline becomes an issue and no member has merged the PR, the test branch developer may accept it themselves.
Resulting test branch: *test/scanner-tests* 


A future implementation possibility could be module-based unit testing and using Git Issues to assign debugging/fix jobs to certain members. This alongside our current approach of opening pull requests that are *not* approved by the same person who opened it. This will ensure consistent testing/code quality assessment throughout the project's timeline.

When running test cases:
1. Ensure you are in ```comp3649-project/imperative``` directory
2. Run the following to test your code
``` sh
python -m unittest -v tests.<test_module>
```
``` sh
# Example
python -m unittest -v tests.scanner-test
```
The ```-v``` flag will print the ```unittest``` results in *verbose* form so you can see exactly which test cases passed and failed.