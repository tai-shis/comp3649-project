import System.Environment (getArgs)
import System.FilePath (takeBaseName)
import System.Directory (createDirectoryIfMissing)
import Data.Char (isDigit)

import Input.Instruction
  ( Instructions,
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
import Intermediate.InterferenceGraph
  ( buildGraph,
    colourGraph,
    getColouring,
  )
import Intermediate.Liveness
  ( determineLiveness,
    isLive,
    getLivenessName,
  )
import Output.Assembly (Assembly)
import Output.AssemblyGenerator
  ( generateAssembly,
  )

-- Private: runs generation process.
gen :: Int -> String -> IO ()
gen registers inputFile = do
  putStrLn "Scanning and parsing through input file..."
  scanner <- createScanner inputFile
  tokens <- scanAll scanner
  -- putStrLn "=== Tokens ==="
  -- mapM_ (putStrLn . tokenListToString) tokens
  let instructions = parse tokens
  -- putStrLn "=== Instructions ==="
  putStrLn "Generating instructions..."
  -- print instructions
  -- putStrLn "=== Liveness ==="
  putStrLn "Determining liveness..."
  let liveness = determineLiveness instructions
  let initialLiveVars = map getLivenessName (filter isLive (head liveness))
  -- putStrLn (showLivenessStates liveness)

  putStrLn "Building interference graph..."
  let graph = buildGraph (getAllVariables instructions) liveness
  putStrLn "Colouring graph..."
  let colourings = colourGraph graph registers
  putStrLn "Generating assembly..."
  let assembly = generateAssembly (getInstructions instructions) initialLiveVars (getLiveVariables instructions) (getColouring colourings)
  -- putStrLn "=== Assembly ==="
  writeAssembly assembly inputFile

-- Private: Checks given args and returns the two valid inputs
getValidArgs :: [String] -> (Int, String)
getValidArgs [registers, inputFile] = if all isDigit registers
  then (read registers, inputFile)
  else error "Usage: gen <registers> <input-file>"
getValidArgs _ = error "Usage: gen <registers> <input-file>"

-- Private: write assembly to output file derived from input file name.
writeAssembly :: Assembly -> String -> IO ()
writeAssembly assembly inputFile = do
  let outputFile = "./Generated/" ++ takeBaseName inputFile ++ ".s"
  createDirectoryIfMissing True "./Generated"
  putStrLn ("Writing assembly to " ++ outputFile)
  writeFile outputFile (show assembly)


main :: IO ()
main = do
  args <- getArgs
  let (registers, inputFile) = getValidArgs args
  gen registers inputFile
