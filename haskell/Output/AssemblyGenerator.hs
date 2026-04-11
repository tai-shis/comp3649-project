module Output.AssemblyGenerator (
    generateAssembly,
    -- testAssembly
) where

import Input.Token (
    Token,
    TokenType(Literal),
    getValue,
    getType)

import Input.Instruction (
    Instruction(
        BinaryIns,
        UnaryIns,
        AssignmentIns),
    InstructionType(..))

import Intermediate.InterferenceGraph (
    RegisterMap)

import Output.Assembly (
    OpCode(
        ADD,
        SUB,
        MUL,
        DIV,
        MOV),
    AssemblyInstruction(AssemblyInstruction),
    Assembly(Assembly))

-- imports specifically for testing
import Input.Instruction (getInstructions)
-- import Intermediate.InterferenceGraph (is, testColourGraph)

-- Public: loops through all our instructions, translates them, and adds final stores for live variables
generateAssembly :: [Instruction] -> [String] -> [String] -> RegisterMap -> Assembly
generateAssembly instructions liveOnEntry liveOnExit registerMap =
    let -- creating MOVs for variables that need to be in registers at the start
        loadLiveOnEntry = [AssemblyInstruction MOV var (getRegister var registerMap) | var <- liveOnEntry, getRegister var registerMap /= var]
        -- translating the math instructions
        body = concatMap (\instruction -> generateSingleAsm instruction registerMap) instructions
        -- creating MOVs for variables that must be stored back to memory at the end
        storeLiveOnExit = [AssemblyInstruction MOV (getRegister var registerMap) var | var <- liveOnExit, getRegister var registerMap /= var]
    in Assembly (loadLiveOnEntry ++ body ++ storeLiveOnExit)

-- Private: pattern matches based on the type of instructions given (binary,unary, or assignment) and converts to assembly appropriately
generateSingleAsm :: Instruction -> RegisterMap -> [AssemblyInstruction]
generateSingleAsm (BinaryIns _ destination operand1 operator operand2) registerMap
    -- case 1: the first operand is already in the destination register
    | source1String == destString = [AssemblyInstruction finalOpCode source2String destString]
    -- case 2: the second operand is in the destination register (if operation is ADD or MUL we swap order to avoid overwriting source data and saving a MOV instruction)
    | source2String == destString && (finalOpCode == ADD || finalOpCode == MUL) =
        [AssemblyInstruction finalOpCode source1String destString]
    -- case 3: keep the default behaviour
    | otherwise = [AssemblyInstruction MOV source1String destString, AssemblyInstruction finalOpCode source2String destString]
    where destString    = getOperand destination registerMap
          source1String = getOperand operand1 registerMap
          source2String = getOperand operand2 registerMap
          finalOpCode   = getOpCode operator

generateSingleAsm (UnaryIns _ destination operator operand) registerMap =
    if getValue operator == "-" then
        if sourceString == destString then
            [AssemblyInstruction MUL "#-1" destString] -- skips the MOV instruction and just negates the register (as the dead variable and the new variable are assigned at the same time)
        else
            [AssemblyInstruction MOV sourceString destString, AssemblyInstruction MUL "#-1" destString]
    else
        if sourceString == destString then
            [] -- skips the redundand MOV instruction
        else
            [AssemblyInstruction MOV sourceString destString]
    where destString   = getOperand destination registerMap
          sourceString = getOperand operand registerMap

generateSingleAsm (AssignmentIns _ destination operand) registerMap =
    if sourceString == destString then
        [] -- if the dead variable and the new variable are assigned to the same register at the same time, skip
    else
        [AssemblyInstruction MOV sourceString destString]
    where destString   = getOperand destination registerMap
          sourceString = getOperand operand registerMap

-- Private: helper function to find out if we are dealing with a literal (1,2,3,4,etc) or a register (a,b,c,d,e,etc)
getOperand :: Token -> RegisterMap -> String
getOperand token registerMap =
    if getType token == Literal then
        "#" ++ getValue token
    else
        getRegister (getValue token) registerMap

-- Private: helper function to loop through our register dictionary to find out which register a variable belongs to
getRegister :: String -> RegisterMap -> String
getRegister variableName [] = variableName  -- if the variable isn't in the map, just return it (prevents crashing)
getRegister variableName ((knownVariable, assignedRegister):remainingMap) =
    if variableName == knownVariable then
        "R" ++ show assignedRegister
    else
        getRegister variableName remainingMap

-- Private: translates our string operators into the appropriate assembly data type
getOpCode :: Token -> OpCode
getOpCode token
    | operatorString == "+" = ADD
    | operatorString == "-" = SUB
    | operatorString == "*" = MUL
    | operatorString == "/" = DIV
    | otherwise             = ADD
    where operatorString = getValue token
