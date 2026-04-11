'''
Run this file for testing.
'''
import sys
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph
from generator.asm_generator import ASMGenerator

TEST_DIR = "tests/test-output/"
REG_COUNT = 8
# Helpers
def get_generator(input_file: str, num_regs: int) -> ASMGenerator:
    file = open_file(input_file)
    parser = Parser(Scanner(file))
    
    try:
        instruction_buffer = parser.parse()
    except ValueError as ve:
        print(f"Error parsing input: {ve}")
        sys.exit(1)
    
    liveness = Liveness(instruction_buffer)
    variables = instruction_buffer.get_occurred_variables()
    interference_graph = InterferenceGraph()
    interference_graph.build_graph(liveness, variables)
    print(liveness.liveness_info())
    
    try:
        interference_graph.color_graph(num_regs)
    except ValueError as ve:
        print(f"Error colouring graph: {ve}")
        sys.exit(1)
    
    interference_graph.print_variable_interference_table()
    interference_graph.print_register_colouring_table(num_regs)

    return ASMGenerator(instruction_buffer, interference_graph, liveness)

def open_file(input_file: str):
    try:
        file = open("test-input/" + input_file, 'r')
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit(1)
    return file

def test_assignments():
    generator: ASMGenerator = get_generator("assignments.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "assignments.s")

def test_binary_ops_with_literals():
    generator: ASMGenerator = get_generator("binary_ops_with_literals.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "binary_ops_with_literals.s")

def test_binary_ops():
    generator: ASMGenerator = get_generator("binary_ops.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "binary_ops.s")

def test_chained_reuse():
    generator: ASMGenerator = get_generator("chained_reuse.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "chained_reuse.s")

def test_empty_file():
    generator: ASMGenerator = get_generator("empty_file.txt", REG_COUNT)    
    generator.generate_assembly(TEST_DIR + "empty_file.s")

def test_invalid_operators():
    generator: ASMGenerator = get_generator("invalid_operators.txt", REG_COUNT)    
    generator.generate_assembly(TEST_DIR + "invalid_operators.s")

def test_malformed_in_middle():
    generator: ASMGenerator = get_generator("malformed_in_middle.txt", REG_COUNT)    
    generator.generate_assembly(TEST_DIR + "malformed_in_middle.s")

def test_malformed_syntax():
    generator: ASMGenerator = get_generator("malformed_syntax.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "malformed_syntax.s")

def test_missing_operands():
    generator: ASMGenerator = get_generator("missing_operands.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "missing_operands.s")

def test_mixed_all_types():
    generator: ASMGenerator = get_generator("mixed_all_types.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "mixed_all_types.s")

def test_multiple_live_vars():
    generator: ASMGenerator = get_generator("multiple_live_vars.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "multiple_live_vars.s")

def test_no_live_declaration():
    generator: ASMGenerator = get_generator("no_live_declaration.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "no_live_declaration.s")

def test_reference_program():
    generator: ASMGenerator = get_generator("reference_program.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "reference_program.s")

def test_single_assignment():
    generator: ASMGenerator = get_generator("single_assignment.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "single_assignment.s")

def test_single_binary():
    generator: ASMGenerator = get_generator("single_binary.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "single_binary.s")

def test_single_unary():
    generator: ASMGenerator = get_generator("single_unary.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "single_unary.s")

def test_unary_ops():
    generator: ASMGenerator = get_generator("unary_ops.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "unary_ops.s")

def test_undefined_variables():
    generator: ASMGenerator = get_generator("undefined_variables.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "undefined_variables.s")

def test_valid_then_invalid_operator():
    generator: ASMGenerator = get_generator("valid_then_invalid_operator.txt", REG_COUNT)
    generator.generate_assembly(TEST_DIR + "valid_then_invalid_operator.s")

if __name__ == "__main__":
    test_assignments() # Want successful ASM output - Success
    test_binary_ops_with_literals() # Want successful ASM output - Success
    test_binary_ops() # Want successful ASM output - Success
    test_chained_reuse() # Want successful ASM output - Success
    test_empty_file() # Want empty '.s' file - Success
    
    try:
        test_invalid_operators() # Looking for error - Error confirmed
    except:
        print("Error successfully")
    
    try:
        test_malformed_syntax() # Looking for error - Error confirmed    
    except:
        print("Error successfully")
    
    try:
        test_missing_operands() # Looking for error - Error confirmed 
    except ValueError as ve:
        print("Error successfully")

    test_mixed_all_types() # Want successful ASM output - Success
    test_multiple_live_vars() # Want successful ASM output - Success
    test_no_live_declaration() # Want ASM output with no MOV back into memory at the end of the output - Success
    test_reference_program() # Want something similar to D2L example - Success. 4 registers are used. D2L example uses 7, optimized D2L version uses 2
    test_single_assignment() # Looking for assignment and then a move back into memory - Success
    test_single_binary() # Looking for MOV, ADD, then MOV back to save program state - Success
    test_single_unary() # Looking for MOV, MUL #-1, MOV - Success
    test_unary_ops() # Looking for multiple instances similar to last test - Success
    test_undefined_variables() # Looking for two MOV into separate registers, add those registers, then MOV back to memory - Success
    try:
        test_valid_then_invalid_operator() # Looking for an error to be raised in the console - Success
    except:
        print("Error successfully")