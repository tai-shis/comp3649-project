
from io import StringIO
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer
from intermediate.liveness import Liveness
from intermediate.interference_graph import InterferenceGraph

def liveness_test():
    # Example usage
    input_data = StringIO("a=a+1\nt1=a*4\nt2=t1+1\nt3=a*3\nb=t2-t3\nt4=b/2\nd=c+t4\nlive: d")
    scanner = Scanner(input_data)
    parser = Parser(scanner)

    try:
        instruction_buffer = parser.parse()
    except ValueError as ve:
        print(f"Parsing error: {ve}")


    liveness = Liveness(instruction_buffer)

    ig_test(liveness, instruction_buffer)

def liveness_test2():
    input_data = StringIO("b=a+1\nd=b*2\ne=4-d\nb=e\nc=5\nf=b-1\nlive: c, e")
    scanner = Scanner(input_data)
    parser = Parser(scanner)

    try:
        instruction_buffer = parser.parse()
    except ValueError as ve:
        print(f"Parsing error: {ve}")


    liveness = Liveness(instruction_buffer)

    ig_test(liveness, instruction_buffer)

def liveness_test3():
    input_data = StringIO("a=a+1\nt1=a*2\nb=t1/3\nlive: a, b")
    scanner = Scanner(input_data)
    parser = Parser(scanner)

    try:
        instruction_buffer: InstructionBuffer = parser.parse()
    except ValueError as ve:
        print(f"Parsing error: {ve}")


    liveness = Liveness(instruction_buffer)

    ig_test(liveness, instruction_buffer)

def ig_test(liveness: Liveness, instruction_buffer: InstructionBuffer):
    interference_graph = InterferenceGraph()
    variables = instruction_buffer.get_occured_variables()
    interference_graph.build_graph(liveness, variables)

    print(interference_graph)
    

liveness_test2()


