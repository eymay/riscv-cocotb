import sys
import cocotb
# sys.path.append('../../../src/riscv_cocotb/')
from riscv_cocotb.unit_test_instrs import generate_tests_for_type, RTypeInstr, ITypeInstr
from riscv_cocotb.instr_types import Arch


#### Test Generator ####

# Generates tests with minimal configuration for a maximum number of instructions

simple_core_arch = Arch(custom_modules={
    "regfile": "regfile",
    "alu": "funit",
}, littleEndian=False)

generate_tests_for_type(RTypeInstr, simple_core_arch)
generate_tests_for_type(ITypeInstr, simple_core_arch)


##### Expressive Tests ####
# Useful for debugging and isolating tests

from riscv_cocotb.generic_tests import generic_itype_test, generic_rtype_test

@cocotb.test()
async def addi_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: x + y, "addi")


@cocotb.test()
async def slti_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: 1 if x < y else 0, "slti")


@cocotb.test()
async def sltiu_test(dut):
    await generic_itype_test(
        dut, simple_core_arch, lambda x, y: 1 if (x + 2**32) < (y + 2**32) else 0, "sltiu"
    )


@cocotb.test()
async def xori_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: x ^ y, "xori")


@cocotb.test()
async def ori_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: x | y, "ori")


@cocotb.test()
async def andi_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: x & y, "andi")


# shifts on the value in
# register rs1 by the shift amount held in the lower 5 bits of register rs2
@cocotb.test()
async def slli_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: x << y, "slli")


@cocotb.test()
async def srli_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: (x % 0x100000000) >> y, "srli")


@cocotb.test()
async def srai_test(dut):
    await generic_itype_test(dut, simple_core_arch, lambda x, y: x >> y, "srai")


@cocotb.test()
async def add_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x + y, "add")


@cocotb.test()
async def sub_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x - y, "sub")


# shifts on the value in
# register rs1 by the shift amount held in the lower 5 bits of register rs2
@cocotb.test()
async def sll_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x << y, "sll")


@cocotb.test()
async def slt_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: 1 if x < y else 0, "slt")


@cocotb.test()
async def sltu_test(dut):
    await generic_rtype_test(
        dut, simple_core_arch, lambda x, y: 1 if (x + 2**32) < (y + 2**32) else 0, "sltu"
    )


@cocotb.test()
async def xor_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x ^ y, "xor")


@cocotb.test()
async def srl_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: (x % 0x100000000) >> y, "srl")


@cocotb.test()
async def sra_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x >> y, "sra")


@cocotb.test()
async def or_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x | y, "or")


@cocotb.test()
async def and_test(dut):
    await generic_rtype_test(dut, simple_core_arch, lambda x, y: x & y, "and")
