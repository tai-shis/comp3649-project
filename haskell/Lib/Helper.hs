module Lib.Helper (
    commaSperatedList,
    addList,
    addUnique,
    pairTrue
) where

-- Utility functions for displaying various data structures in a readable format

-- Private: Helper function for commaSperatedList to recursively build the string with commas in front
commaSeperatedRest :: Show a => [a] -> String
commaSeperatedRest (x:xs) = ", " ++ show x ++ commaSeperatedRest xs
commaSeperatedRest [] = ""

-- Public: Converts a list of showable items into a comma-separated string
commaSperatedList :: Show a => [a] -> String
commaSperatedList (x:xs) = show x ++ commaSeperatedRest xs
commaSperatedList [] = ""

-- Public: Adds all elements of the first list to the second list if they are not already present
addList :: (Eq a) => [a] -> [a] -> [a]
addList [] acc = acc
addList (x:xs) acc | elem x acc = addList xs acc
    | otherwise = addList xs (x:acc)

-- Public: Adds element to a list if it is not already present
addUnique :: (Eq a) => a -> [a] -> [a]
addUnique x acc | elem x acc = acc
    | otherwise = x:acc

-- Public: And on a pair of bools
pairTrue :: (Bool, Bool) -> Bool
pairTrue (b1, b2) = b1 && b2