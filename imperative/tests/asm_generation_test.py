import os
import unittest

from generator.asm_generator import ASMGenerator
from generator.asm_instruction import ASMInstruction
from intermediate.interference_graph import InterferenceGraph
from intermediate.liveness import Liveness
from input.instruction import Instruction
from input.instruction_buffer import InstructionBuffer
from input.token import Token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_buffer(instructions: list[Instruction], live_objects: list[str]) -> InstructionBuffer:
    """Helper to build an InstructionBuffer from instructions and live objects."""
    buf = InstructionBuffer()
    for instr in instructions:
        buf.add_instruction(instr)
    for live in live_objects:
        buf.add_live_object(live)
    return buf


def make_graph(colors: dict[str, int | None]) -> InterferenceGraph:
    """Helper to build an InterferenceGraph with a pre-set colors dict."""
    graph = InterferenceGraph()
    graph.colors = colors
    return graph


def make_generator(instructions: list[Instruction],
                   live_objects: list[str],
                   colors: dict[str, int | None]) -> ASMGenerator:
    """Helper that wires together a full ASMGenerator from raw parts."""
    buf = make_buffer(instructions, live_objects)
    graph = make_graph(colors)
    liveness = Liveness(buf)
    return ASMGenerator(buf, graph, liveness)


def make_binary(dest: str, op1: str, op1_type: int,
                operator: str, op2: str, op2_type: int) -> Instruction:
    """Helper to create a binary (type-0) instruction."""
    return Instruction(
        0,
        Token(dest, 0),
        Token(op1, op1_type),
        Token(operator, 3),
        Token(op2, op2_type),
    )


def make_unary(dest: str, operator: str, operand: str, operand_type: int) -> Instruction:
    """Helper to create a unary (type-1) instruction."""
    return Instruction(
        1,
        Token(dest, 0),
        operator=Token(operator, 3),
        operand2=Token(operand, operand_type),
    )


def make_assignment(dest: str, operand: str, operand_type: int) -> Instruction:
    """Helper to create an assignment (type-2) instruction."""
    return Instruction(2, Token(dest, 0), Token(operand, operand_type))


def asm_lines(generator: ASMGenerator) -> list[str]:
    """Returns generated_asm as a list of 'OPCODE op1,op2' strings for easy comparison."""
    return [f"{i.op_code} {i.op1},{i.op2}" for i in generator.generated_asm]


def tmp_path(filename: str) -> str:
    """Returns a path inside a temporary output directory."""
    return os.path.join("output", "test_gen2", filename)


# ---------------------------------------------------------------------------
# Construction tests
# ---------------------------------------------------------------------------

class TestASMGeneratorConstruction(unittest.TestCase):

    def test_fields_initialized(self):
        gen = make_generator([], [], {})
        self.assertEqual(gen.generated_asm, [])
        self.assertEqual(gen.in_register, set())

    def test_register_colors_assigned(self):
        colors = {"a": 0, "b": 1}
        gen = make_generator([], [], colors)
        self.assertEqual(gen.register_colors, colors)

    def test_opcodes_initialized(self):
        gen = make_generator([], [], {})
        expected = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
        self.assertEqual(gen.opcodes, expected)


# ---------------------------------------------------------------------------
# _get_reg() tests
# ---------------------------------------------------------------------------

class TestGetReg(unittest.TestCase):

    def test_variable_assigned_to_r0(self):
        gen = make_generator([], [], {"a": 0})
        self.assertEqual(gen._get_reg(Token("a", 1)), "R0")

    def test_variable_assigned_to_r2(self):
        gen = make_generator([], [], {"b": 2})
        self.assertEqual(gen._get_reg(Token("b", 1)), "R2")

    def test_variable_not_in_colors_raises_error(self):
        gen = make_generator([], [], {})
        with self.assertRaises(ValueError):
            gen._get_reg(Token("z", 1))

    def test_variable_with_none_color_raises_error(self):
        gen = make_generator([], [], {"a": None})
        with self.assertRaises(ValueError):
            gen._get_reg(Token("a", 1))


# ---------------------------------------------------------------------------
# _get_op_code() tests
# ---------------------------------------------------------------------------

class TestGetOpCode(unittest.TestCase):

    def test_addition(self):
        gen = make_generator([], [], {})
        self.assertEqual(gen._get_op_code(Token("+", 3)), "ADD")

    def test_subtraction(self):
        gen = make_generator([], [], {})
        self.assertEqual(gen._get_op_code(Token("-", 3)), "SUB")

    def test_multiplication(self):
        gen = make_generator([], [], {})
        self.assertEqual(gen._get_op_code(Token("*", 3)), "MUL")

    def test_division(self):
        gen = make_generator([], [], {})
        self.assertEqual(gen._get_op_code(Token("/", 3)), "DIV")


# ---------------------------------------------------------------------------
# _load_variable() tests
# ---------------------------------------------------------------------------

class TestLoadVariable(unittest.TestCase):

    def test_literal_returns_empty_list(self):
        gen = make_generator([], [], {})
        result = gen._load_variable(Token("42", 2))
        self.assertEqual(result, [])

    def test_variable_not_resident_emits_mov(self):
        gen = make_generator([], [], {"a": 0})
        result = gen._load_variable(Token("a", 1))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].op_code, "MOV")
        self.assertEqual(result[0].op1, "a")
        self.assertEqual(result[0].op2, "R0")

    def test_variable_not_resident_added_to_in_register(self):
        gen = make_generator([], [], {"a": 0})
        gen._load_variable(Token("a", 1))
        self.assertIn("a", gen.in_register)

    def test_variable_already_resident_returns_empty_list(self):
        gen = make_generator([], [], {"a": 0})
        gen.in_register.add("a")
        result = gen._load_variable(Token("a", 1))
        self.assertEqual(result, [])


# ---------------------------------------------------------------------------
# _get_operand_str() tests
# ---------------------------------------------------------------------------

class TestGetOperandStr(unittest.TestCase):

    def test_literal_returns_hash_prefixed(self):
        gen = make_generator([], [], {})
        self.assertEqual(gen._get_operand_str(Token("42", 2)), "#42")

    def test_variable_returns_register(self):
        gen = make_generator([], [], {"a": 1})
        self.assertEqual(gen._get_operand_str(Token("a", 1)), "R1")


# ---------------------------------------------------------------------------
# _generate_instruction_asm() tests
# ---------------------------------------------------------------------------

class TestGenerateInstructionAsm(unittest.TestCase):

    def _run(self, instr: Instruction, colors: dict, live_objects: list[str] = [],
             extra_instrs: list[Instruction] = []) -> tuple[list[ASMInstruction], ASMGenerator]:
        """Helper to run _generate_instruction_asm on a single instruction."""
        all_instrs = [instr] + extra_instrs
        buf = make_buffer(all_instrs, live_objects)
        graph = make_graph(colors)
        liveness = Liveness(buf)
        gen = ASMGenerator(buf, graph, liveness)
        liveness_list = liveness.get_liveness()
        next_liveness = liveness_list[1] if len(liveness_list) > 1 else {}
        result = gen._generate_instruction_asm(instr, liveness_list[0], next_liveness)
        return result, gen

    def test_binary_in_place_dest_equals_op1(self):
        # a = a + 1, a in R0 — compute in place
        instr = make_binary("a", "a", 1, "+", "1", 2)
        result, _ = self._run(instr, {"a": 0})
        opcodes = [i.op_code for i in result]
        self.assertIn("MOV", opcodes)
        self.assertIn("ADD", opcodes)

    def test_binary_dest_not_equal_op1_emits_mov(self):
        # a = b + 1, a in R0, b in R1
        instr = make_binary("a", "b", 1, "+", "1", 2)
        result, _ = self._run(instr, {"a": 0, "b": 1})
        self.assertTrue(any(i.op_code == "MOV" and i.op2 == "R0" for i in result))
        self.assertTrue(any(i.op_code == "ADD" for i in result))

    def test_binary_commutative_swap_when_dest_equals_op2(self):
        # a = b + a, a in R0, b in R1 — swap since ADD commutes
        instr = make_binary("a", "b", 1, "+", "a", 1)
        result, _ = self._run(instr, {"a": 0, "b": 1})
        add_instr = next(i for i in result if i.op_code == "ADD")
        # After swap, op2 should be R1 (b) and dest R0 (a)
        self.assertEqual(add_instr.op2, "R0")

    def test_binary_non_commutative_conflict_stores_then_reloads(self):
        # a = 1 - a, a in R0 — non-commutative, must store a before overwriting
        instr = make_binary("a", "1", 2, "-", "a", 1)
        result, _ = self._run(instr, {"a": 0})
        opcodes = [i.op_code for i in result]
        self.assertIn("SUB", opcodes)
        # Should have stored a to memory before overwriting R0
        store = next((i for i in result if i.op_code == "MOV" and i.op2 == "a"), None)
        self.assertIsNotNone(store)

    def test_binary_returns_list_of_asm_instructions(self):
        instr = make_binary("a", "a", 1, "+", "1", 2)
        result, _ = self._run(instr, {"a": 0})
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, ASMInstruction)

    def test_binary_adds_dest_to_in_register(self):
        instr = make_binary("a", "a", 1, "+", "1", 2)
        _, gen = self._run(instr, {"a": 0})
        self.assertIn("a", gen.in_register)

    def test_unary_negation_dest_not_equal_source_emits_mov(self):
        # x = -a, x in R1, a in R0
        instr = make_unary("x", "-", "a", 1)
        result, _ = self._run(instr, {"x": 1, "a": 0})
        opcodes = [i.op_code for i in result]
        self.assertIn("MOV", opcodes)
        self.assertIn("MUL", opcodes)
        mul_instr = next(i for i in result if i.op_code == "MUL")
        self.assertEqual(mul_instr.op1, "#-1")

    def test_unary_negation_in_place_no_mov(self):
        # a = -a, a in R0 — in place, no MOV needed
        instr = make_unary("a", "-", "a", 1)
        result, _ = self._run(instr, {"a": 0})
        mov_instrs = [i for i in result if i.op_code == "MOV" and i.op2 == "R0"]
        # Only the initial load MOV should be present, not an extra register-to-register MOV
        for mov in mov_instrs:
            self.assertNotEqual(mov.op1, "R0")

    def test_unary_adds_dest_to_in_register(self):
        instr = make_unary("a", "-", "b", 1)
        _, gen = self._run(instr, {"a": 0, "b": 1})
        self.assertIn("a", gen.in_register)

    def test_assignment_from_variable_emits_mov(self):
        # b = a, a in R0, b in R1
        instr = make_assignment("b", "a", 1)
        result, _ = self._run(instr, {"a": 0, "b": 1})
        self.assertTrue(any(i.op_code == "MOV" and i.op1 == "R0" and i.op2 == "R1" for i in result))

    def test_assignment_same_register_no_extra_mov(self):
        # a = b, a and b both in R0 — no register-to-register MOV needed
        instr = make_assignment("a", "b", 1)
        result, _ = self._run(instr, {"a": 0, "b": 0})
        reg_to_reg = [i for i in result if i.op_code == "MOV" and i.op1 == "R0" and i.op2 == "R0"]
        self.assertEqual(len(reg_to_reg), 0)

    def test_assignment_from_literal(self):
        # a = 42, a in R0
        instr = make_assignment("a", "42", 2)
        result, _ = self._run(instr, {"a": 0})
        self.assertTrue(any(i.op_code == "MOV" and i.op1 == "#42" and i.op2 == "R0" for i in result))

    def test_assignment_adds_dest_to_in_register(self):
        instr = make_assignment("a", "42", 2)
        _, gen = self._run(instr, {"a": 0})
        self.assertIn("a", gen.in_register)

    def test_invalid_instruction_type_returns_empty(self):
        instr = Instruction(-1, Token("x", 0))
        buf = make_buffer([instr], [])
        graph = make_graph({})
        liveness = Liveness(buf)
        gen = ASMGenerator(buf, graph, liveness)
        result = gen._generate_instruction_asm(instr, {}, {})
        self.assertEqual(result, [])

    def test_store_back_triggered_when_sharing_var_becomes_live(self):
        # a = a + 1, t1 = a * 4 — a and t2 share R0, t2 live on next line
        instr1 = make_binary("a", "a", 1, "+", "1", 2)
        instr2 = make_binary("t1", "a", 1, "*", "4", 2)
        colors = {"a": 0, "t1": 1, "t2": 0}
        buf = make_buffer([instr1, instr2], ["t1", "t2"])
        graph = make_graph(colors)
        liveness = Liveness(buf)
        gen = ASMGenerator(buf, graph, liveness)
        liveness_list = liveness.get_liveness()
        next_liveness = liveness_list[1] if len(liveness_list) > 1 else {}
        result = gen._generate_instruction_asm(instr1, liveness_list[0], next_liveness)
        store_back = [i for i in result if i.op_code == "MOV" and i.op2 == "a"]
        self.assertGreater(len(store_back), 0)

    def test_store_back_not_triggered_when_no_conflict(self):
        # a = a + 1, nothing shares R0
        instr = make_binary("a", "a", 1, "+", "1", 2)
        result, _ = self._run(instr, {"a": 0}, live_objects=["a"])
        store_back = [i for i in result if i.op_code == "MOV" and i.op2 == "a"]
        self.assertEqual(len(store_back), 0)


# ---------------------------------------------------------------------------
# _write_live_on_exit() tests
# ---------------------------------------------------------------------------

class TestWriteLiveOnExit(unittest.TestCase):

    def test_single_live_on_exit_variable(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        gen._write_live_on_exit()
        self.assertTrue(any(i.op_code == "MOV" and i.op1 == "R0" and i.op2 == "a"
                            for i in gen.generated_asm))

    def test_multiple_live_on_exit_variables(self):
        instr = make_binary("t1", "a", 1, "+", "b", 1)
        gen = make_generator([instr], ["a", "b"], {"a": 0, "b": 1, "t1": 2})
        gen._write_live_on_exit()
        store_ops = [i for i in gen.generated_asm if i.op_code == "MOV"]
        stored_vars = [i.op2 for i in store_ops]
        self.assertIn("a", stored_vars)
        self.assertIn("b", stored_vars)

    def test_no_live_on_exit_variables(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], [], {"a": 0})
        gen._write_live_on_exit()
        self.assertEqual(gen.generated_asm, [])


# ---------------------------------------------------------------------------
# generate_assembly() integration tests
# ---------------------------------------------------------------------------

class TestGenerateAssembly(unittest.TestCase):

    def test_returns_list_of_asm_instructions(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        result = gen.generate_assembly(tmp_path("returns_list.s"))
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, ASMInstruction)

    def test_file_created(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        path = tmp_path("file_created.s")
        gen.generate_assembly(path)
        self.assertTrue(os.path.exists(path))

    def test_file_format_correct(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        path = tmp_path("file_format.s")
        gen.generate_assembly(path)
        with open(path) as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
        for line in lines:
            parts = line.split(" ", 1)
            self.assertEqual(len(parts), 2)
            self.assertIn(",", parts[1])

    def test_creates_missing_directories(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        path = tmp_path("subdir/nested/test.s")
        gen.generate_assembly(path)
        self.assertTrue(os.path.exists(path))

    def test_single_assignment_literal(self):
        # a = 42, live: a
        # Expected: MOV #42,R0 / MOV R0,a
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        gen.generate_assembly(tmp_path("single_assign.s"))
        lines = asm_lines(gen)
        self.assertIn("MOV #42,R0", lines)
        self.assertIn("MOV R0,a", lines)

    def test_single_unary(self):
        # a = -b, live: a — separate registers
        instr = make_unary("a", "-", "b", 1)
        gen = make_generator([instr], ["a"], {"a": 0, "b": 1})
        gen.generate_assembly(tmp_path("single_unary.s"))
        lines = asm_lines(gen)
        self.assertIn("MOV b,R1", lines)
        self.assertIn("MUL #-1,R0", lines)
        self.assertIn("MOV R0,a", lines)

    def test_single_binary_separate_registers(self):
        # a = b + c, live: a — all separate registers
        instr = make_binary("a", "b", 1, "+", "c", 1)
        gen = make_generator([instr], ["a"], {"a": 0, "b": 1, "c": 2})
        gen.generate_assembly(tmp_path("single_binary.s"))
        lines = asm_lines(gen)
        self.assertTrue(any("ADD" in l for l in lines))
        self.assertIn("MOV R0,a", lines)

    def test_chained_same_register_no_reloads(self):
        # a = a + 1, a = a - 1 — a in R0 throughout, no reloads needed
        instrs = [
            make_binary("a", "a", 1, "+", "1", 2),
            make_binary("a", "a", 1, "-", "1", 2),
        ]
        gen = make_generator(instrs, ["a"], {"a": 0})
        gen.generate_assembly(tmp_path("chained_same_reg.s"))
        lines = asm_lines(gen)
        # a should only be loaded once at the start
        load_count = sum(1 for l in lines if l == "MOV a,R0")
        self.assertEqual(load_count, 1)

    def test_unary_chain_all_same_register(self):
        # a = -b, t1 = -a, t2 = -t1, live: t2 — all share R0
        instrs = [
            make_unary("a", "-", "b", 1),
            make_unary("t1", "-", "a", 1),
            make_unary("t2", "-", "t1", 1),
        ]
        gen = make_generator(instrs, ["t2"], {"a": 0, "b": 0, "t1": 0, "t2": 0})
        gen.generate_assembly(tmp_path("unary_chain.s"))
        lines = asm_lines(gen)
        mul_count = sum(1 for l in lines if l == "MUL #-1,R0")
        self.assertEqual(mul_count, 3)
        self.assertIn("MOV R0,t2", lines)

    def test_assignments_pipeline(self):
        # a=b, a=3, b=100, c=a, d=c, live: d
        # R0: a,c,d  R1: b
        instrs = [
            make_assignment("a", "b", 1),
            make_assignment("a", "3", 2),
            make_assignment("b", "100", 2),
            make_assignment("c", "a", 1),
            make_assignment("d", "c", 1),
        ]
        gen = make_generator(instrs, ["d"], {"a": 0, "b": 1, "c": 0, "d": 0})
        gen.generate_assembly(tmp_path("assignments.s"))
        lines = asm_lines(gen)
        # d must be stored on exit
        self.assertIn("MOV R0,d", lines)
        # literal assignments correct
        self.assertIn("MOV #3,R0", lines)
        self.assertIn("MOV #100,R1", lines)

    def test_live_on_exit_stored(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], ["a"], {"a": 0})
        gen.generate_assembly(tmp_path("live_exit.s"))
        lines = asm_lines(gen)
        self.assertIn("MOV R0,a", lines)

    def test_not_live_on_exit_not_stored(self):
        instr = make_assignment("a", "42", 2)
        gen = make_generator([instr], [], {"a": 0})
        gen.generate_assembly(tmp_path("not_live_exit.s"))
        lines = asm_lines(gen)
        store_backs = [l for l in lines if l == "MOV R0,a"]
        self.assertEqual(len(store_backs), 0)

    def test_correct_instruction_order(self):
        # Instructions should appear in program order in generated_asm
        instrs = [
            make_assignment("a", "1", 2),
            make_assignment("b", "2", 2),
            make_assignment("c", "3", 2),
        ]
        gen = make_generator(instrs, ["c"], {"a": 0, "b": 1, "c": 2})
        gen.generate_assembly(tmp_path("order.s"))
        lines = asm_lines(gen)
        idx_a = next(i for i, l in enumerate(lines) if "R0" in l and "#1" in l)
        idx_b = next(i for i, l in enumerate(lines) if "R1" in l and "#2" in l)
        idx_c = next(i for i, l in enumerate(lines) if "R2" in l and "#3" in l)
        self.assertLess(idx_a, idx_b)
        self.assertLess(idx_b, idx_c)

if __name__ == "__main__":
    unittest.main(verbosity=2)