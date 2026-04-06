module Tests.InterferenceGraphTest where

import Data.Set (empty, fromList, toList)
import Input.Token
import Input.Instruction
import Intermediate.Liveness hiding (Live)
import qualified Intermediate.Liveness as L
import Intermediate.InterferenceGraph

-- Helper to report pass/fail
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- Helper: check if a variable in a graph has a specific neighbor
hasNeighbor :: Graph -> String -> String -> Bool
hasNeighbor graph varName neighborName =
    case filter (\v -> getName v == varName) (getVertices graph) of
        []    -> False
        (v:_) -> neighborName `elem` toList (getNeighbors v)

-- Helper: check if a variable exists in the graph
hasVertex :: Graph -> String -> Bool
hasVertex graph varName = any (\v -> getName v == varName) (getVertices graph)

-- A simple graph with two connected nodes for reuse
twoNodeGraph :: Graph
twoNodeGraph = addEdge (Graph [createVariable "a", createVariable "b"]) "a" "b"

-- Sample liveness states for buildGraph tests
singleLiveLine :: [LivenessStates]
singleLiveLine = [[L.Live "a", L.Live "b"]]

mixedLiveLine :: [LivenessStates]
mixedLiveLine = [[L.Live "a", L.Unlive "b"]]

testInterferenceGraph :: IO ()
testInterferenceGraph = mapM_ putStrLn results

results :: [String]
results =
    
    [
        -- createVariable
        check "createVariable - correct name" (getName (createVariable "x") == "x"),
        check "createVariable - empty neighbors" (getNeighbors (createVariable "x") == empty),

        -- createGraph
        check "createGraph - empty vertices" (getVertices createGraph == []),

        -- Show Variable
        check "Show Variable - no neighbors" (show (createVariable "x") == "x -> "),
        check "Show Variable - with neighbors" (show (head (filter (\v -> getName v == "a") (getVertices twoNodeGraph))) == "a -> \"b\"")
        ++ (show (head (filter (\v -> getName v == "a") (getVertices twoNodeGraph)))),

        -- Show Graph
        check "Show Graph - empty graph" (show createGraph == "Interference Graph: \n"),
        check "Show Graph - populated graph"
            (let g = show twoNodeGraph
            in "Interference Graph: \n" `isPrefixOf` g
                && "a -> \"b\"" `isInfixOf` g
                && "b -> \"a\"" `isInfixOf` g),

        -- Eq Variable
        check "Eq Variable - equal variables" (createVariable "x" == createVariable "x"),
        check "Eq Variable - different names" (createVariable "x" /= createVariable "y"),

        -- Eq Graph
        check "Eq Graph - equal graphs" (createGraph == createGraph),
        check "Eq Graph - different graphs" (Graph [createVariable "x"] /= Graph [createVariable "y"]),

        -- addEdge
        check "addEdge - both nodes exist, a has b as neighbor" (hasNeighbor twoNodeGraph "a" "b"),
        check "addEdge - both nodes exist, b has a as neighbor" (hasNeighbor twoNodeGraph "b" "a"),
        check "addEdge - first node missing" 
            (addEdge (Graph [createVariable "b"]) "a" "b"
            == Graph [createVariable "b"]),
        check "addEdge - second node missing"
            (addEdge (Graph [createVariable "a"]) "a" "b"
            == Graph [createVariable "a"]),
        check "addEdge - neither node exists" (addEdge createGraph "a" "b" == createGraph),
        check "addEdge - self edge" 
            (let g = Graph [createVariable "x"]
            in addEdge g "x" "x" == g),
        check "addEdge - duplicate edge"
            (let g  = Graph [createVariable "a", createVariable "b"]
                 g1 = addEdge g  "a" "b"
                 g2 = addEdge g1 "a" "b"
                in g1 == g2),
        check "addEdge - three nodes, a-b and a-c edges"
            (let g  = Graph [createVariable "a", createVariable "b", createVariable "c"]
                 g1 = addEdge g  "a" "b"
                 g2 = addEdge g1 "a" "c"
                in hasNeighbor g2 "a" "b"
                && hasNeighbor g2 "a" "c"
                && hasNeighbor g2 "b" "a"
                && hasNeighbor g2 "c" "a"
                && not (hasNeighbor g2 "b" "c")),

        -- buildGraph
        check "buildGraph - empty variables and liveness" (buildGraph [] [] == createGraph),
        check "buildGraph - nodes created for all variables"
            (let g = buildGraph ["a", "b", "x"] []
            in hasVertex g "a" && hasVertex g "b" && hasVertex g "x"),
        check "buildGraph - edge between two live vars"
            (let g = buildGraph ["a", "b"] singleLiveLine
            in hasNeighbor g "a" "b" && hasNeighbor g "b" "a"),
        check "buildGraph - no edge for unlive variable"
            (let g = buildGraph ["a", "b"] mixedLiveLine
            in not (hasNeighbor g "a" "b") && not (hasNeighbor g "b" "a")),
        check "buildGraph - no edge for isolated variable"
            (let g = buildGraph ["a", "b", "x"] singleLiveLine
            in getNeighbors (head (filter (\v -> getName v == "x") (getVertices g))) == empty),
        check "buildGraph - no duplicate edges"
            (let doubleLive = [singleLiveLine !! 0, singleLiveLine !! 0]
                 g = buildGraph ["a", "b"] doubleLive
                in toList (getNeighbors (head (filter (\v -> getName v == "a") (getVertices g)))) == ["b"]),
        check "buildGraph - no self edges"
            (let g = buildGraph ["a"] [[L.Live "a"]]
            in getNeighbors (head (getVertices g)) == empty)
    ]

-- String helpers
isPrefixOf :: String -> String -> Bool
isPrefixOf [] _  = True
isPrefixOf _  [] = False
isPrefixOf (x:xs) (y:ys) = x == y && isPrefixOf xs ys

isInfixOf :: String -> String -> Bool
isInfixOf needle haystack = any (isPrefixOf needle) (tails haystack)

tails :: [a] -> [[a]]
tails []         = [[]]
tails xs@(_:rest) = xs : tails rest