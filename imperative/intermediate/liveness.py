from llist import dllist
from input.instruction_buffer import InstructionBuffer, Instruction
from input.scanner import Token

class Liveness:
    # Possible states for a variable listed in our liveness analysis
    state = {
        "defined": 0,
        "live": 1
    }

    def __init__(self, instruction_buffer: InstructionBuffer) -> None:
        
        # { a: 0, t1: 1, etc... } where 0 is defined and 1 is live. (according to the current line)
        self.liveness: dllist = dllist() # list of dicts of line-by-line liveness
        self.instruction_buffer: InstructionBuffer = instruction_buffer

        self._determine_liveness()

    def _mark_liveness(self, variables: list[Token], line_liveness: dict[str, int], carry_vars: list[str]) -> None:
        """
        Marks the liveness of a set of variables.
        
        :param instruction: The instruction to analyze.
        :type instruction: Instruction
        :param line_liveness: The current line's liveness dictionary.
        :type line_liveness: dict[str, int]
        :param carry_vars: The list of carry variables from the previous line.
        :type carry_vars: list[str]
        """

        # First, we mark any carry variables as live in this line
        for c in carry_vars:
            line_liveness[c] = self.state["live"]
        # Make sure to clear the carry var array
        carry_vars.clear()

        # Check for any variables in the line
        match len(variables):
            case 3:
                line_liveness[variables[1].value] = self.state["live"]
                line_liveness[variables[2].value] = self.state["live"]
            case 2:
                line_liveness[variables[1].value] = self.state["live"]

        # Destination is always a variable (index 0)
        line_liveness[variables[0].value] = self.state["defined"]

        # Repopulate carry vars
        for var, state in line_liveness.items():
            if state == self.state["live"]:
                carry_vars.append(var)

    def _determine_initial_liveness(self) -> list[str]:
        """
        Determines the initial liveness of variables based on the live objects specified
        at the end of the instruction buffer.

        :return: A list of variables that are live after the last instruction.
        :rtype: list[str]
        """
        line_liveness: dict[str, int] = {}
        carry_vars: list[str] = []

        for live in self.instruction_buffer.list_live_objects():
            line_liveness[live] = self.state["live"]
            carry_vars.append(live) # We carry these forward to the previous line (itll make sense later)

        self.liveness.appendleft(line_liveness)

        return carry_vars

    def _determine_liveness(self) -> None:
        """
        Determines the liveness state of variables in the instruction buffer.
        """
        
        # This algorithm is freaky, will try to comment it as best as possible
        carry_vars: list[str] = [] # Holds variables that were were live and not defined in the last line, 

        # First, determine liveness for after this code block (found in the live: etc. section)
        # and also get any carry variables (i.e. variables that are live)
        carry_vars = self._determine_initial_liveness()
        # Here, carry vars are just what is after "live: " in the input stream

        # We iterate backwards, finding the last use of a variable, then marking when it gets defined
        for instruction in reversed(self.instruction_buffer.list_instructions()):
            line_liveness: dict[str, int] = {} # Holds liveness for the current line

            # Okay, we now have to grab all the variables in the line
            variables: list[Token] = instruction.get_variables()
            
            # Now we can mark liveness
            self._mark_liveness(variables, line_liveness, carry_vars)
            # Appending left to reverse the order as we go
            self.liveness.appendleft(line_liveness)

    def liveness_info(self) -> list[str]:
        """
        Retrieves the liveness information as a list of strings.

        :return: A list of strings representing the liveness information.
        :rtype: list[str]
        """
        liveness_strings: list[str] = []

        for line_liveness in self.liveness:
            line_string = "["
            for var, state in line_liveness.items():
                state_str = "defined" if state == self.state["defined"] else "live"
                line_string += f"{var}: {state_str}, "
            liveness_strings.append(f"{line_string[:-2]}]")

        return liveness_strings

    def __str__(self) -> str:
        string = ""

        instructions = self.instruction_buffer.list_instructions()
        liveness_info = self.liveness_info()

        for i, line in enumerate(instructions):
            string += f"{i}: {line}: {liveness_info[i]}\n"

        string += f"{len(instructions)}: End of code block: {liveness_info[-1]}\n"

        return string

            