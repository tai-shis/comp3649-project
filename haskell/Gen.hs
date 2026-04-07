import Input.Token (
    TokenType(
        Destination,
        Variable,
        Literal,
        Operator),
    createToken)

import Input.Instruction (
    Instructions,
    createInstruction, 
    fromArraysInstructions,
    getAllVariables,
    getInstructions)

import Intermediate.Liveness (
    determineLiveness,
    livenessInfo,
    showLivenessStates)

import Intermediate.InterferenceGraph (
    Variable(..), 
    Graph(..),
    createVariable, 
    getName, 
    getNeighbors, 
    createGraph, 
    getVertices, 
    addEdge,
    buildGraph,
    Register,
    RegisterMap,
    colourGraph,
    getColouring)

import Output.AssemblyGenerator (
    generateAssembly)


-- TEST DATA
ins1 = createInstruction (createToken "a"  Destination, createToken "a"  Variable, createToken "+"  Operator, createToken "1"  Literal)
ins2 = createInstruction (createToken "t1" Destination, createToken "a"  Variable, createToken "*"   Operator, createToken "4"  Literal)
ins3 = createInstruction (createToken "t2" Destination, createToken "t1" Variable, createToken "+"  Operator, createToken "1"  Literal)
ins4 = createInstruction (createToken "t3" Destination, createToken "a"  Variable, createToken "*"   Operator, createToken "3"  Literal)
ins5 = createInstruction (createToken "b"  Destination, createToken "t2" Variable, createToken "-"  Operator, createToken "t3" Variable)
ins6 = createInstruction (createToken "t4" Destination, createToken "b"  Variable, createToken "/"  Operator, createToken "2"  Literal)
ins7 = createInstruction (createToken "d"  Destination, createToken "c"  Variable, createToken "+"  Operator, createToken "t5" Variable)

is = fromArraysInstructions [ins1, ins2, ins3, ins4, ins5, ins6, ins7] ["d"]

-- Private: runs generation process.
gen :: Int -> Instructions -> IO ()
gen registers instructions = do
    let liveness = determineLiveness instructions
    let graph = buildGraph (getAllVariables instructions) liveness
    let colourings = colourGraph graph registers
    let assembly = generateAssembly (getInstructions instructions) (getColouring colourings)
    print assembly

main :: IO ()
main = gen 5 is