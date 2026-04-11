module Lib.Helper (
    commaSeparatedList,
    addList,
    addUnique,
    pairTrue
) where

-- Utility functions for displaying various data structures in a readable format

-- Private: Helper function for commaSeperatedList to recursively build the string with commas in front
commaSeparatedRest :: Show a => [a] -> String
commaSeparatedRest (x:xs) = ", " ++ show x ++ commaSeparatedRest xs
commaSeparatedRest [] = ""

-- Public: Converts a list of showable items into a comma-separated string
commaSeparatedList :: Show a => [a] -> String
commaSeparatedList (x:xs) = show x ++ commaSeparatedRest xs
commaSeparatedList [] = ""

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