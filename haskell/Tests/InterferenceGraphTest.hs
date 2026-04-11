module Tests.InterferenceGraphTest where

import Data.Set (empty, fromList, toList)
import Input.Token
import Input.Instruction
import Intermediate.Liveness hiding (Live)
import qualified Intermediate.Liveness as L
import Intermediate.InterferenceGraph

-- standard wrapper
check :: String -> Bool -> String
check name True  = "PASS: " ++ name
check name False = "FAIL: " ++ name

-- quick way to check if a specific edge exists
hasNeighbor :: Graph -> String -> String -> Bool
hasNeighbor graph varName neighborName =
    case filter (\v -> getName v == varName) (getVertices graph) of
        []    -> False
        (v:_) -> neighborName `elem` toList (getNeighbors v)

-- check if a node even exists
hasVertex :: Graph -> String -> Bool
hasVertex graph varName = any (\v -> getName v == varName) (getVertices graph)

-- dummy graph for reuse so we don't build from scratch every time
twoNodeGraph :: Graph
twoNodeGraph = addEdge (Graph [createVariable "a", createVariable "b"]) "a" "b"

-- dummy liveness states for the builder
singleLiveLine :: [LivenessStates]
singleLiveLine = [[L.Live "a", L.Live "b"]]

mixedLiveLine :: [LivenessStates]
mixedLiveLine = [[L.Live "a", L.Unlive "b"]]

main :: IO ()
main = mapM_ putStrLn results

results :: [String]
results =
    [
        -- node creation
        check "create node saves name correctly" (getName (createVariable "x") == "x"),
        check "new node starts with no neighbors" (getNeighbors (createVariable "x") == empty),

        -- empty graph
        check "new graph is completely empty" (getVertices createGraph == []),

        -- printing
        check "print lonely variable" (show (createVariable "x") == "x -> "),
        check "print connected variable" 
            (let v = head (filter (\x -> getName x == "a") (getVertices twoNodeGraph))
             in show v == "a -> \"b\""),

        check "print empty graph" (show createGraph == "Interference Graph: \n"),
        check "print graph shows all connections"
            (let g = show twoNodeGraph
            in "Interference Graph: \n" `isPrefixOf` g
                && "a -> \"b\"" `isInfixOf` g
                && "b -> \"a\"" `isInfixOf` g),

        -- equality
        check "same variables are equal" (createVariable "x" == createVariable "x"),
        check "different variables are not" (createVariable "x" /= createVariable "y"),

        check "empty graphs are equal" (createGraph == createGraph),
        check "different graphs are not" (Graph [createVariable "x"] /= Graph [createVariable "y"]),

        -- manual edge adding
        check "adding edge connects a to b" (hasNeighbor twoNodeGraph "a" "b"),
        check "adding edge connects b back to a" (hasNeighbor twoNodeGraph "b" "a"),
        check "adding edge fails quietly if first node is missing" 
            (addEdge (Graph [createVariable "b"]) "a" "b"
            == Graph [createVariable "b"]),
        check "adding edge fails quietly if second node is missing"
            (addEdge (Graph [createVariable "a"]) "a" "b"
            == Graph [createVariable "a"]),
        check "adding edge fails quietly if graph is empty" (addEdge createGraph "a" "b" == createGraph),
        
        check "self edges are ignored" 
            (let g = Graph [createVariable "x"]
            in addEdge g "x" "x" == g),
            
        check "duplicate edges don't break anything"
            (let g  = Graph [createVariable "a", createVariable "b"]
                 g1 = addEdge g  "a" "b"
                 g2 = addEdge g1 "a" "b"
                in g1 == g2),
                
        check "multiple connections on one node work"
            (let g  = Graph [createVariable "a", createVariable "b", createVariable "c"]
                 g1 = addEdge g  "a" "b"
                 g2 = addEdge g1 "a" "c"
                in hasNeighbor g2 "a" "b"
                && hasNeighbor g2 "a" "c"
                && hasNeighbor g2 "b" "a"
                && hasNeighbor g2 "c" "a"
                && not (hasNeighbor g2 "b" "c")),

        -- the main builder function
        check "builder handles empty inputs" (buildGraph [] [] == createGraph),
        check "builder creates all requested nodes"
            (let g = buildGraph ["a", "b", "x"] []
            in hasVertex g "a" && hasVertex g "b" && hasVertex g "x"),
            
        check "builder connects things alive at same time"
            (let g = buildGraph ["a", "b"] singleLiveLine
            in hasNeighbor g "a" "b" && hasNeighbor g "b" "a"),
            
        check "builder ignores dead variables"
            (let g = buildGraph ["a", "b"] mixedLiveLine
            in not (hasNeighbor g "a" "b") && not (hasNeighbor g "b" "a")),
            
        check "isolated variable stays lonely"
            (let g = buildGraph ["a", "b", "x"] singleLiveLine
            in getNeighbors (head (filter (\v -> getName v == "x") (getVertices g))) == empty),
            
        check "builder doesn't double-connect over multiple lines"
            (let doubleLive = [singleLiveLine !! 0, singleLiveLine !! 0]
                 g = buildGraph ["a", "b"] doubleLive
                in toList (getNeighbors (head (filter (\v -> getName v == "a") (getVertices g)))) == ["b"]),
                
        check "builder prevents self interference"
            (let g = buildGraph ["a"] [[L.Live "a"]]
            in getNeighbors (head (getVertices g)) == empty)
    ]

-- dumb string helpers for the print tests
isPrefixOf :: String -> String -> Bool
isPrefixOf [] _  = True
isPrefixOf _  [] = False
isPrefixOf (x:xs) (y:ys) = x == y && isPrefixOf xs ys

isInfixOf :: String -> String -> Bool
isInfixOf needle haystack = any (isPrefixOf needle) (tails haystack)

tails :: [a] -> [[a]]
tails []         = [[]]
tails xs@(_:rest) = xs : tails rest