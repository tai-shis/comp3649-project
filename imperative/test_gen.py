import sys
from io import StringIO
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph
from generator.asm_generator import ASMGenerator

TEST_DIR = "tests/test-output/"

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
    
    try:
        interference_graph.color_graph(num_regs)
    except ValueError as ve:
        print(f"Error colouring graph: {ve}")
        sys.exit(1)
    
    interference_graph.print_variable_interference_table()
    interference_graph.print_register_colouring_table(num_regs)

    return ASMGenerator(instruction_buffer, interference_graph)

def open_file(input_file: str):
    try:
        file = open("tests/test-input/" + input_file, 'r')
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit(1)
    return file

def test_assignments():
    generator: ASMGenerator = get_generator("assignments.txt", 4)
    generator.generate_assembly(TEST_DIR + "assignments.s")

def test_binary_ops_with_literals():
    generator: ASMGenerator = get_generator("binary_ops_with_literals.txt", 3)
    generator.generate_assembly(TEST_DIR + "binary_ops_with_literals.s")

def test_binary_ops():
    generator: ASMGenerator = get_generator("binary_ops.txt", 3)
    generator.generate_assembly(TEST_DIR + "binary_ops.s")

def test_chained_reuse():
    generator: ASMGenerator = get_generator("chained_reuse.txt", 2)
    generator.generate_assembly(TEST_DIR + "chained_reuse.s")

def test_empty_file():
    generator: ASMGenerator = get_generator("empty_file.txt", 2)    
    generator.generate_assemb

def test_invalid_operators():
    generator: ASMGenerator = get_generator("invalid_operators.txt", 4)    
    generator.generate_assembly(TEST_DIR + "invalid_operators.s")

def test_malformed_in_middle():
    generator: ASMGenerator = get_generator("malformed_in_middle.txt", 4)    
    generator.generate_assembly(TEST_DIR + "malformed_in_middle.s")

if __name__ == "__main__":
    # test_assignments()
    # test_binary_ops_with_literals()
    # test_binary_ops()
    # test_chained_reuse()
    # test_empty_file()
    test_invalid_operators()
