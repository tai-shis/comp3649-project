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
<small>Last Updated: 22/01/2026</small>

#### Interference Graph

### Week 5
<small>Last Updated: 22/01/2026</small>

#### Graph-Colouring Algorithm

## High-level Design Architecture
<small>Last Updated: 22/01/2026</small>

### Main Data Structures
- Token
- Scanner
- Parser
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