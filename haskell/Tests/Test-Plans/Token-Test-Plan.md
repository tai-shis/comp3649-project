# Token Test Plan

| Category (Reason) | Test (Input) | Expected Output | Actual Output |
|:------------------|:-------------|:----------------|:--------------|
| getters | `getValue` on variable | `"x"` | `"x"` **PASS** |
| getters | `getType` on destination | `Destination` | `Destination` **PASS** |
| creation | make Variable token | `Variable` type | correct **PASS** |
| creation | make Literal token | `Literal` type | correct **PASS** |
| creation | make Operator token | `Operator` type | correct **PASS** |
| creation | make Equals token | `Equals` type | correct **PASS** |
| creation | make Live token | `Live` type | correct **PASS** |
| creation | make LiveSymbol token | `LiveSymbol` type | correct **PASS** |
| creation | make Newline token | `Newline` type | correct **PASS** |
| creation | make EOF token | `EOF` type | correct **PASS** |
| extraction | `getValue` on abc | `"abc"` | `"abc"` **PASS** |
| extraction | `getValue` on EOF | `""` (empty string) | `""` **PASS** |
| extraction | `getValue` on operator | `"+"` | `"+"` **PASS** |
| extraction | `getType` on dest | `Destination` | `Destination` **PASS** |
| extraction | `getType` on literal | `Literal` | `Literal` **PASS** |
| extraction | `getType` on EOF | `EOF` | `EOF` **PASS** |
| printing types | `show Destination` | `"Destination"` | prints fine **PASS** |
| printing types | `show Variable` | `"Variable"` | prints fine **PASS** |
| printing types | `show Literal` | `"Literal"` | prints fine **PASS** |
| printing types | `show Operator` | `"Operator"` | prints fine **PASS** |
| printing types | `show Equals` | `"Equals"` | prints fine **PASS** |
| printing types | `show Live` | `"Live"` | prints fine **PASS** |
| printing types | `show LiveSymbol` | `"LiveSymbol"` | prints fine **PASS** |
| printing types | `show Newline` | `"Newline"` | prints fine **PASS** |
| printing types | `show EOF` | `"EOF"` | prints fine **PASS** |
| printing tokens| show variable token | `"x : Variable"` | `"x : Variable"` **PASS** |
| printing tokens| show literal token | `"42 : Literal"` | `"42 : Literal"` **PASS** |
| printing tokens| show operator token | `"+ : Operator"` | `"+ : Operator"` **PASS** |
| printing tokens| show EOF token | `" : EOF"` | `" : EOF"` **PASS** |
| equality | identical tokens | `True` | `True` **PASS** |
| inequality | different values | `False` | `False` **PASS** |
| inequality | different types | `False` | `False` **PASS** |
| inequality | completely different | `False` | `False` **PASS** |
| type equality | `Variable == Variable` | `True` | `True` **PASS** |
| type inequality| `Variable /= Literal` | `False` | `False` **PASS** |