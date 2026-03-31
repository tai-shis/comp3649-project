module InterferenceGraph (
    Variable, 
    Graph, 
    createVariable, 
    getName, 
    getNeighbors, 
    createGraph, 
    getVertices, 
    addEdge
) where


import Data.Set (Set, toList, empty, insert)
import Instruction (Instruction, getVariables)
import Display

type Neighbors = Set String


-- Variables name, and their neighbors (just the names)
data Variable = Variable (String, Neighbors)
    deriving (Eq)

instance Show Variable where
    show (Variable (name, neighbors)) = name ++ " -> " ++ commaSperatedList (toList neighbors)

data Graph = Graph [Variable]
    deriving (Eq)

instance Show Graph where
    show (Graph vertices) = "Interference Graph: \n" ++ concatMap (\v -> show v ++ "\n") vertices

-- Public: Creates a variable given a name
createVariable :: String -> Variable
createVariable name = Variable (name, empty)

-- Public: Gets the name of a variable
getName :: Variable -> String
getName (Variable (name, _)) = name

-- Public: Gets the neighbors of a variable 
getNeighbors :: Variable -> Neighbors
getNeighbors (Variable (_, neighbors)) = neighbors

-- Public: Creates an empty graph
createGraph :: Graph
createGraph = Graph []

-- Public: Gets the vertices of a graph
getVertices :: Graph -> [Variable]
getVertices (Graph vertices) = vertices

-- Private: Given two variable names, updates the neighbors of a variable if it matches either name
updateNeighbors :: String -> String -> Variable -> Variable
updateNeighbors name1 name2 var = if name == name1 then Variable (name, insert name2 neighbors)
    else if name == name2 then Variable (name, insert name1 neighbors)
    else var
    where name = getName var
          neighbors = getNeighbors var


-- Private: Checks if two variables exist in the graph
edgeExists :: [Variable] -> String -> String -> (Bool, Bool)
edgeExists [] _ _ = (False, False)
edgeExists (v:vs) name1 name2 | name1 == name2 = (False, False)
    | otherwise = (name == name1 || fst rest, name == name2 || snd rest)
        where rest = edgeExists vs name1 name2
              name = getName v

-- Private: And on a pair of bools
pairTrue :: (Bool, Bool) -> Bool
pairTrue (b1, b2) = b1 && b2

-- Public: Adds an edge between two variables in the graph if they both exist, otherwise returns the original graph
addEdge :: Graph -> String -> String -> Graph
addEdge graph name1 name2 | pairTrue (edgeExists (getVertices graph) name1 name2) = Graph (map (updateNeighbors name1 name2) (getVertices graph))
    | otherwise = graph

