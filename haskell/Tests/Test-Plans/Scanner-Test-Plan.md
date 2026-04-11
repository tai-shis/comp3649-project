# Scanner-Test-Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| **EOF Handling** — `scanNextLine` on an empty file should immediately set state to `ScanEOF` | Empty file (`empty.txt`) | `scanningState = ScanEOF` | |
| **EOF Handling** — After the last line is consumed, the next `scanNextLine` call should return `ScanEOF` | Single-line file (`test_single_line.txt`), call `scanNextLine` twice | First call: state `Live`, buffer non-empty; Second call: `scanningState = ScanEOF` | |
| **State Detection** — Line beginning with `live:` token should yield `Live` state | Line: `live: x = 1` | `scanningState = Live` | |
| **State Detection** — Line beginning with a non-`Live`/non-`EOF` token should yield `Instructions` state | Line: `add x, y` | `scanningState = Instructions` | |
| **Delimiter — space** — Spaces split tokens but do not produce a token themselves | Line: `x y` | Tokens: `x`, `y`; no space token | |
| **Delimiter — comma** — Commas split tokens but do not produce a token themselves | Line: `x,y` | Tokens: `x`, `y`; no comma token | |
| **Delimiter — equals** — `=` is tokenized as its own `Equals` token and flips `isDestination` to `False` | Line: `x = 1` | Tokens: `x` (Destination), `=` (Equals), `1` (Literal) | |
| **Delimiter — colon** — `:` is only valid as the suffix of `live:` and should be consumed as part of that token | Line: `live: x = 1` | Token `live:` of type `Live`; no standalone `:` token | |
| **Delimiter — colon (error)** — A bare `:` not preceded by `live` should throw an error | Line: `x: y` | `error "Unexpected ':' found in token: 'x:'"` | |
| **Operator Tokenization** — Each operator should become its own `Operator` token and split surrounding symbols | Line: `a+b` | Tokens: `a`, `+`, `b` | |
| **Operator Tokenization** — All four operators in one expression | Line: `a+b-c*d/e` | Tokens: `a`, `+`, `b`, `-`, `c`, `*`, `d`, `/`, `e` | |
| **Operator Tokenization** — Operator at the start of a line (no leading symbol) | Line: `+x` | Tokens: `+`, `x`; no empty/blank token before `+` | |
| **Operator Tokenization** — Operator at the end of a line (no trailing symbol) | Line: `x+` | Tokens: `x`, `+`; no empty/blank token after `+` | |
| **Invalid Characters** — Any invalid character (e.g. `$`) should throw an error | Line: `x$y` | `error "Invalid character '$' found in input."` | |
| **Invalid Characters** — Line consisting entirely of invalid characters should throw an error | Line: `$!@#` | `error "Invalid character '$' found in input."` | |
| **Token Types — Literal** — An all-digit string should produce a `Literal` token | Line: `123` | Single token `123` of type `Literal` | |
| **Token Types — Destination** — First variable before `=` in an `Instructions`-state scanner should be typed `Destination` | Line: `result = 1` (Instructions state) | Token `result` of type `Destination` | |
| **Token Types — Variable** — Variable appearing after `=` should be typed `Variable` (`isDestination` flips to `False` after `=`) | Line: `result = x` (Instructions state) | Token `x` of type `Variable` | |
| **Token Types — LiveSymbol** — Variable in a `Live`-state scanner should be typed `LiveSymbol` | Line: `live: x = 1` | Token `x` of type `LiveSymbol` | |
| **Token Types — Operator** — Single-char operator string should produce type `Operator` | Line: `a+b` | Token `+` of type `Operator` | |
| **Token Types — Equals** — `=` should produce type `Equals` | Line: `x = 1` | Token `=` of type `Equals` | |
| **Symbol Accumulation — leftover flush** — Symbol still accumulating when line ends should be flushed as a token (base case of `scanChars`) | Line: `abc` (no trailing delimiter or operator) | Single token `abc` | |
| **Variable Validation — digit-leading (error)** — A variable starting with a digit but containing letters should throw an error | Line: `1x = 2` | `error "Invalid token: '1x'."` | |
| **Empty Line** — A blank line should yield an empty buffer | Line: `` (empty string) | `buffer = []` | |
| **Whitespace-Only Line** — A line of only spaces should yield an empty buffer | Line: `   ` | `buffer = []` | |
| **Multi-token realistic line** — Full `live:` instruction with operators | Line: `live: result = a+b` | Tokens: `live:` (Live), `result` (LiveSymbol), `=` (Equals), `a` (LiveSymbol), `+` (Operator), `b` (LiveSymbol); state `Live` | |
| **Multi-line advancement** — Scanner correctly advances line-by-line, updating buffer on each call | File with 3 distinct lines (`test_multiline.txt`) | Each `scanNextLine` call produces the correct buffer for that line; final call gives `ScanEOF` | |