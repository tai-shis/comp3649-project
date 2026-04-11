# Scanner Test Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| file io | empty file | `scanningState == ScanEOF` | matches expected **PASS** |
| state machine | live keyword seen | `scanningState == Live` | state flipped **PASS** |
| delimiters | `"x y"` (spaces) | skips space, gets `["x", "y"]` | ignored space **PASS** |
| delimiters | `"x = 1"` | gets equals sign as own token | extracted equals **PASS** |
| delimiters | colon suffix | consumes colon into `"live:"` | colon absorbed **PASS** |
| bad input | `"x: y"` (bare colon) | throws unexpected token error | crashes safely **PASS** |
| operators | `"a+b"` | gets `["a", "+", "b"]` | split correctly **PASS** |
| operators | massive chain | extracts all 9 tokens perfectly | split correctly **PASS** |
| operators | edge limits (`"+x"`, `"x+"`) | handles missing sides | handled safely **PASS** |
| bad input | `"x$y"` | throws invalid char error | crashes safely **PASS** |
| bad input | `"$!@#"` (all garbage) | throws invalid char error | crashes safely **PASS** |
| bad input | `"1x = 2"` | throws leading digit error | crashes safely **PASS** |
| tagging | `"123"` | tags as `Literal` | tagged correctly **PASS** |
| tagging | `"result = 1"` | tags `result` as `Destination` | tagged correctly **PASS** |
| tagging | `"result = x"` | tags `x` as `Variable` | tagged correctly **PASS** |
| tagging | `"live: x = 1"` | tags `x` as `LiveSymbol` | tagged correctly **PASS** |
| edge cases | `"abc"` (no trailing delim) | doesn't drop the last token | kept token **PASS** |
| edge cases | completely blank string | leaves the token buffer empty | empty buffer **PASS** |
| integration | `"live: result = a+b"` | perfect breakdown and Live state | works perfectly **PASS** |
