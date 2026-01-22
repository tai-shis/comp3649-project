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
#### Graph-Colouring Algorithm

## High-level Design Architecture

## High-level Testing Framework