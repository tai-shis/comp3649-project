import Input.Instruction
  ( Instructions,
    createInstruction,
    fromArraysInstructions,
    getAllVariables,
    getInstructions,
    getLiveVariables,
  )
import Input.Parser
  ( parse,
  )
import Input.Scanner
  ( createScanner,
    scanAll,
  )
import Input.Token
  ( TokenType
      ( Destination,
        Literal,
        Operator,
        Variable
      ),
    createToken,
    tokenListToString,
  )
import Intermediate.InterferenceGraph
  ( Graph (..),
    Register,
    RegisterMap,
    Variable (..),
    addEdge,
    buildGraph,
    colourGraph,
    createGraph,
    createVariable,
    getColouring,
    getName,
    getNeighbors,
    getVertices,
  )
import Intermediate.Liveness
  ( determineLiveness,
    livenessInfo,
    showLivenessStates,
    isLive,
    getLivenessName
  )
import Output.AssemblyGenerator
  ( generateAssembly,
  )

-- Private: runs generation process.
gen :: Int -> IO ()
gen registers = do
  putStrLn "Scanning and parsing through input file..."
  scanner <- createScanner "Tests/Test-Inputs/input1.txt"
  tokens <- scanAll scanner
  -- putStrLn "=== Tokens ==="
  -- mapM_ (putStrLn . tokenListToString) tokens
  let instructions = parse tokens
  putStrLn "=== Instructions ==="
  putStrLn "Generating instructions..."
  print instructions
  putStrLn "=== Liveness ==="
  putStrLn "Determining liveness..."
  let liveness = determineLiveness instructions
  let initialLiveVars = map getLivenessName (filter isLive (head liveness))
  putStrLn (showLivenessStates liveness)

  putStrLn "Building interference graph..."
  let graph = buildGraph (getAllVariables instructions) liveness
  putStrLn "Colouring graph..."
  let colourings = colourGraph graph registers
  putStrLn "Generating assembly..."
  let assembly = generateAssembly (getInstructions instructions) initialLiveVars (getLiveVariables instructions) (getColouring colourings)
  putStrLn "=== Assembly ==="
  print assembly

main :: IO ()
main = gen 5
