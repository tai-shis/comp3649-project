
import sys
from io import StringIO
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph
from generator.asm_generator import ASMGenerator

def main():
    """
    Generates assembly code from a three-address code input file, given a specified number of registers.

    :param args: Command-line arguments, where the first argument is the number of registers and the second is the input file path.
    :type args: list[str]
    :return: Exit code, where 0 indicates success and -1 indicates an error.
    :rtype: int
    """
    args = sys.argv[1:]
    
    if len(args) != 2:
        print("Usage: gen <num_regs> <input_file>")
        sys.exit(1)
    
    num_regs, input_file = args

    if not num_regs.isdigit() or int(num_regs) <= 0:
        print("Number of registers must be a positive integer.")
        sys.exit(1) 
    
    try: 
        file = open(input_file, 'r')
    except FileNotFoundError:
        print(f"File not found: {input_file}")
        sys.exit(1)
    
    print(f"Generating assembly code from {input_file} using {num_regs} registers...")
    scanner = Scanner(file)
    parser = Parser(scanner)

    try:
        instruction_buffer = parser.parse()
    except ValueError as ve:
        print(f"Error parsing input: {ve}")
        sys.exit(1)

    print("Successfully parsed input. Now performing liveness analysis and graph coloring...")

    # Get the information for the graph
    liveness = Liveness(instruction_buffer)
    variables = instruction_buffer.get_occured_variables()

    # Now build the graph
    interference_graph = InterferenceGraph()
    interference_graph.build_graph(liveness, variables)

    # And then, we can color it
    try:
        interference_graph.color_graph(int(num_regs))
    except ValueError as ve:
        print(f"Error coloring graph: {ve}")
        sys.exit(1)
    
    print("\nGraph successfully colored. Now generating assembly code...\n")

    interference_graph.print_variable_interference_table()
    interference_graph.print_register_colouring_table(int(num_regs))

    generator = ASMGenerator(instruction_buffer, interference_graph)
    
    generator.generate_assembly(input_file)

    print(f"Assembly code generated successfully to {input_file}.s")


main()

