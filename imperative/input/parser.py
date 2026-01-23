from instruction_buffer import InstructionBuffer
from scanner import Scanner

class Parser:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
