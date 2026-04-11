{-# LANGUAGE ScopedTypeVariables #-}
module Tests.ScannerTest where

import System.IO
import System.Directory (removeFile, doesFileExist)
import Control.Exception (try, SomeException, evaluate)
import Input.Scanner
import Input.Token (Token(Tn))
import qualified Input.Token as T

-- simple wrapper so a single bad file doesn't crash the whole test suite
check :: String -> IO Bool -> IO String
check name (action :: IO Bool) = do
    result <- try action :: IO (Either SomeException Bool)
    case result of
        Right True  -> return ("PASS: " ++ name)
        Right False -> return ("FAIL: " ++ name)
        Left _      -> return ("FAIL: " ++ name ++ " (threw an exception)")

-- specifically for testing things that SHOULD crash
checkCrash :: String -> IO Scanner -> IO String
checkCrash name action = do
    result <- try $ do
        sc <- action
        -- forces Haskell to actually look at every token to find errors
        -- mapM_ behaves like a "for each" loop in python
        mapM_ (\t -> evaluate (show t)) (buffer sc)
        return sc
    case result of
        Left (_ :: SomeException) -> return ("PASS: " ++ name)
        Right _ -> return ("FAIL: " ++ name ++ " (it was supposed to crash!!)")

-- helper to write a string to a file and scan it immediately
scanString :: String -> IO Scanner
scanString content = do
    writeFile "temp_test.txt" content
    sc <- createScanner "temp_test.txt"
    sc' <- scanNextLine sc
    hClose (fileHandle sc')
    return sc'

getVals :: Scanner -> [String]
getVals sc = map (\(Tn v _) -> v) (buffer sc)

getTypes :: Scanner -> [T.TokenType]
getTypes sc = map (\(Tn _ t) -> t) (buffer sc)

main :: IO ()
main = do
    results <- sequence tests
    mapM_ putStrLn results

    -- cleanup (sometimes windows locks the file, so we check first)
    exists <- doesFileExist "temp_test.txt"
    if exists then removeFile "temp_test.txt" else return ()

tests :: [IO String]
tests =
    [
        -- basic state transitions
        check "empty file -> eof" $ do
            sc <- scanString ""
            return $ scanningState sc == ScanEOF,

        check "live keyword switches state" $ do
            sc <- scanString "live: x = 1"
            return $ scanningState sc == Live,

        -- splitting and delimiters
        check "spaces split tokens" $ do
            sc <- scanString "x y"
            return $ getVals sc == ["x","y"],

        check "= shows up as its own token" $ do
            sc <- scanString "x = 1"
            return $ getVals sc == ["x","=","1"]
                && getTypes sc == [T.Destination, T.Equals, T.Literal],

        check "live keeps the colon attached" $ do
            sc <- scanString "live: x = 1"
            return $ "live:" `elem` getVals sc
                && ":" `notElem` getVals sc,

        -- our new simplified crash tests
        checkCrash "random standalone colon should blow up" (scanString "x: y"),

        check "plus splits correctly" $ do
            sc <- scanString "a+b"
            return $ getVals sc == ["a","+","b"],

        check "massive chain of operators" $ do
            sc <- scanString "a+b-c*d/e"
            return $ getVals sc == ["a","+","b","-","c","*","d","/","e"],

        check "operator at the start" $ do
            sc <- scanString "+x"
            return $ getVals sc == ["+","x"],

        check "operator at the end" $ do
            sc <- scanString "x+"
            return $ getVals sc == ["x","+"],

        checkCrash "$ shouldn't be allowed" (scanString "x$y"),

        checkCrash "just complete garbage symbols" (scanString "$!@#"),

        checkCrash "vars can't start with a number" (scanString "1x = 2"),

        -- token typing logic
        check "numbers become literals" $ do
            sc <- scanString "123"
            return $ getTypes sc == [T.Literal],

        check "first var is tagged as destination" $ do
            sc <- scanString "result = 1"
            return $ head (getTypes sc) == T.Destination,

        check "rhs var is just a variable" $ do
            sc <- scanString "result = x"
            return $ last (getTypes sc) == T.Variable,

        check "live vars get tagged as livesymbols" $ do
            sc <- scanString "live: x = 1"
            return $ getTypes sc !! 1 == T.LiveSymbol,

        -- edge cases
        check "single token stays intact" $ do
            sc <- scanString "abc"
            return $ getVals sc == ["abc"],

        check "empty line -> empty buffer" $ do
            sc <- scanString ""
            return $ null (buffer sc),

        check "spaces only -> empty buffer" $ do
            sc <- scanString "    "
            return $ null (buffer sc),

        check "full realistic example parses perfectly" $ do
            sc <- scanString "live: result = a+b"
            return $ getVals sc == ["live:","result","=","a","+","b"]
                && scanningState sc == Live
    ]
