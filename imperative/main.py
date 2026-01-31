
from io import StringIO
from input.scanner import Scanner
from input.parser import Parser
from input.instruction_buffer import InstructionBuffer
from intermediate.liveness import Liveness

# Example usage
input_data = StringIO("a=a+1\nt1=a*4\nt2=t1+1\nt3=a*3\nb=t2-t3\nt4=b/2\nd=c+t4\nlive: d")
scanner = Scanner(input_data)
parser = Parser(scanner)

try:
    instruction_buffer = parser.parse()
except ValueError as ve:
    print(f"Parsing error: {ve}")


liveness = Liveness(instruction_buffer)

print(liveness)