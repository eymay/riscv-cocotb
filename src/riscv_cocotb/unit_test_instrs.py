import cocotb
import inspect
import random
import sys

import riscv_cocotb.debug_utils as dbg
from riscv_cocotb.generic_tests import initialize, set_instruction
from riscv_cocotb.generic_tests import generic_itype_test, generic_rtype_test


from riscv_cocotb.instr_types import Instruction

from cocotb.triggers import FallingEdge, Timer


class mem_type:
    def __init__(self, dut, rs1, offset, len, opstring):
        self.rs1_idx = rs1
        self.rs1 = dut.dp.regfile.regs[rs1]
        self.offset = offset
        self.byte_addr = 0
        self.transf_value = 0
        self.mem = 0

        self.dut = dut

    def check_x0(self, reg, value):
        # x0 register is hardwired to 0 in RISC-V
        return 0 if reg == 0 else value

    def set_rs1(self, value):
        self.rs1.value = self.check_x0(self.rs1_idx, value)
        self.ideal_operand1 = value

    def set_addr(self):
        self.byte_addr = self.rs1.value + self.offset

    def set_memref(self):
        self.mem = self.dut.data_mem.dmem[self.byte_addr]

    def set_mem(self, val):
        self.mem.value = val


class load_type(mem_type):
    def __init__(self, dut, rd, rs1, offset, len, opstring):
        super().__init__(dut, rs1, offset, len, opstring)
        self.rd_idx = rd
        self.rd = dut.dp.regfile.regs[rd]
        self.instr = Instruction(opstring, f"x{rd}", str(offset) + f"(x{rs1})", "")

    def get_value(self):
        print("mem:", self.mem)
        print("mem buff:", self.mem.buff)
        self.transf_value = self.mem[len - 1 : 0].value

    def check_rd(self):
        self.get_value()
        assert (
            self.rd.value == self.transf_value
        ), f"Loaded value not correct {self.rd.value}!={self.transf_value}"


async def generic_load_test(dut, len, opstring, debug=False):
    await initialize(dut)
    rd = 1
    rs1 = 2
    offset = 4
    addr = 4

    instr_obj = load_type(dut, rd, rs1, offset, len, opstring)
    instr_obj.set_rs1(5)
    instr_obj.set_memref()
    set_instruction(instr_obj, dut, addr)

    # debug_instr(dut, addr)

    await FallingEdge(dut.clk)
    if debug:
        dbg.debug_signals(dut, addr)
    # debug_shifter(dut)
    instr_obj.check_rd()

    # debug_instr(dut, addr)

    dut.PC.Q.value = 4

operations = {
    "addi": lambda x, y: x + y,
    "slti": lambda x, y: 1 if x < y else 0,
    "sltiu": lambda x, y: 1 if (x + 2**32) < (y + 2**32) else 0,
    "xori": lambda x, y: x ^ y,
    "ori": lambda x, y: x | y,
    "andi": lambda x, y: x & y,
    "slli": lambda x, y: x << y,
    "srli": lambda x, y: (x % 0x100000000) >> y,
    "srai": lambda x, y: x >> y,
    "add": lambda x, y: x + y,
    "sub": lambda x, y: x - y,
    "sll": lambda x, y: x << y,
    "slt": lambda x, y: 1 if x < y else 0,
    "sltu": lambda x, y: 1 if (x + 2**32) < (y + 2**32) else 0,
    "xor": lambda x, y: x ^ y,
    "srl": lambda x, y: (x % 0x100000000) >> y,
    "sra": lambda x, y: x >> y,
    "or": lambda x, y: x | y,
    "and": lambda x, y: x & y,
}

class BaseInstr:
    def __init__(self, op_name, operation):
        self.op_name = op_name
        self.operation = operation

    async def generic_test(self, dut, arch):
        raise NotImplementedError("Must be implemented by subclass.")

class RTypeInstr(BaseInstr):
    async def generic_test(self, dut, arch):
        await generic_rtype_test(dut, arch, self.operation, self.op_name)

class ITypeInstr(BaseInstr):
    async def generic_test(self, dut, arch):
        await generic_itype_test(dut, arch, self.operation, self.op_name)

class LTypeInstr(BaseInstr):
    async def generic_test(self, dut, arch):
        # L-type specific test logic
        pass

operations_map = {
    op_name: ITypeInstr(op_name, operation) if op_name.endswith("i") or op_name.endswith("iu") 
            else LTypeInstr(op_name, operation) if op_name == "lw" 
            else RTypeInstr(op_name, operation)
    for op_name, operation in operations.items()
}

def test_factory(op_name, instr_instance, arch):
    """Function factory to create and return a test function."""

    @cocotb.test()
    async def test(dut):
        await instr_instance.generic_test(dut, arch)

    test.__name__ = f"test_{op_name}"
    test.__qualname__ = f"test_{op_name}"

    return test

def run_all_tests(arch):
    for op_name, instr_instance in operations_map.items():

        test_func = test_factory(op_name, instr_instance, arch)
        
        # Add the test to the globals to make it discoverable by cocotb
        globals()[test.__name__] = test

def generate_tests_for_type(instr_type_class, arch):
    """
    Generate and register tests for all operations of a specific instruction type
    without requiring an explicit module argument.
    """
    # Determine the caller's module using inspect
    caller_frame = inspect.currentframe().f_back
    caller_module = inspect.getmodule(caller_frame)
    module_globals = caller_module.__dict__

    for op_name, instr_instance in operations_map.items():
        if isinstance(instr_instance, instr_type_class):
            test_func = test_factory(op_name, instr_instance, arch)
            # Add the test to the caller's module globals
            module_globals[test_func.__name__] = test_func

# @cocotb.test(skip=True)
# async def lw_test(dut):
#     await generic_load_test(dut, len=32, opstring="lw", debug=False)
#
#
# @cocotb.test(skip=True)
# async def lh_test(dut):
#     await generic_load_test(dut, len=16, opstring="lh", debug=False)
#
#
# @cocotb.test()
# async def addi_test(dut):
#     await generic_itype_test(dut, lambda x, y: x + y, "addi", debug=False)
#
#
# @cocotb.test()
# async def slti_test(dut):
#     await generic_itype_test(dut, lambda x, y: 1 if x < y else 0, "slti")
#
#
# @cocotb.test()
# async def sltiu_test(dut):
#     await generic_itype_test(
#         dut, lambda x, y: 1 if (x + 2**32) < (y + 2**32) else 0, "sltiu"
#     )
#
#
# @cocotb.test()
# async def xori_test(dut):
#     await generic_itype_test(dut, lambda x, y: x ^ y, "xori")
#
#
# @cocotb.test()
# async def ori_test(dut):
#     await generic_itype_test(dut, lambda x, y: x | y, "ori")
#
#
# @cocotb.test()
# async def andi_test(dut):
#     await generic_itype_test(dut, lambda x, y: x & y, "andi")
#
#
# # shifts on the value in
# # register rs1 by the shift amount held in the lower 5 bits of register rs2
# @cocotb.test()
# async def slli_test(dut):
#     await generic_itype_test(dut, lambda x, y: x << y, "slli")
#
#
# @cocotb.test()
# async def srli_test(dut):
#     await generic_itype_test(dut, lambda x, y: (x % 0x100000000) >> y, "srli")
#
#
# # Immediate generation has error
# # 0100000 shamt[4:0] src SRAI dest OP-IMM
# @cocotb.test(expect_fail=True)
# async def srai_test(dut):
#     await generic_itype_test(dut, lambda x, y: x >> y, "srai")
#
#
# @cocotb.test()
# async def add_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x + y, "add")
#
#
# @cocotb.test()
# async def sub_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x - y, "sub")
#
#
# # shifts on the value in
# # register rs1 by the shift amount held in the lower 5 bits of register rs2
# @cocotb.test()
# async def sll_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x << y, "sll")
#
#
# @cocotb.test()
# async def slt_test(dut):
#     await generic_rtype_test(dut, lambda x, y: 1 if x < y else 0, "slt")
#
#
# @cocotb.test()
# async def sltu_test(dut):
#     await generic_rtype_test(
#         dut, lambda x, y: 1 if (x + 2**32) < (y + 2**32) else 0, "sltu"
#     )
#
#
# @cocotb.test()
# async def xor_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x ^ y, "xor")
#
#
# @cocotb.test()
# async def srl_test(dut):
#     await generic_rtype_test(dut, lambda x, y: (x % 0x100000000) >> y, "srl")
#
#
# @cocotb.test()
# async def sra_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x >> y, "sra")
#
#
# @cocotb.test()
# async def or_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x | y, "or")
#
#
# @cocotb.test()
# async def and_test(dut):
#     await generic_rtype_test(dut, lambda x, y: x & y, "and")
