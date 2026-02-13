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

## High-level Design Architecture
<small>Last Updated: 12/02/2026</small>

### Main Data Structures
- Token
- Scanner
- Parser
- Instruction Buffer
#### Description
The Scanner will read from the input file line by line and create a Token object for every symbol it sees. The Scanner will also be responsible for removing any whitespace, ensuring that whitespace does not affect the outcome of the program. 

Example:
```
a = a + 1
# Will have the same meaning and have the same outcome after tokenization as:
a     = a                + 1
```

The Parser is then responsible for requesting Tokens from the Parser one-by-one and identifying (a) If the Token is valid, and (b) the type of Token it is.

Once the Parser has identified the Token, it will build up a list of these Tokens into lists of instructions.

If at any point the Parser identifies (a) an *invalid symbol*, or (b) invalid ordering of symbols (i.e. a = a -) would be invalid as there is nothing to subtract from the variable 'a', the Parser will throw an exception.

### Modules

## High-level Testing Framework
<small>Last Updated: 22/01/2026</small>

With the current state of the project, our testing framework is to develop test cases as we go.

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